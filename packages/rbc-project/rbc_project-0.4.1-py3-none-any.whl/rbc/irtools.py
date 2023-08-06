# Author: Pearu Peterson
# Created: February 2019

import re
from llvmlite import ir
import llvmlite.binding as llvm
from .targetinfo import TargetInfo
from .npy_mathimpl import *  # noqa: F403, F401
from .utils import get_version
if get_version('numba') >= (0, 49):
    from numba.core import codegen, cpu, compiler_lock, \
        registry, typing, compiler, sigutils, cgutils, \
        extending
    from numba.core import types as nb_types
else:
    from numba.targets import codegen, cpu, registry
    from numba import compiler_lock, typing, compiler, \
        sigutils, cgutils, extending
    from numba import types as nb_types

int32_t = ir.IntType(32)


def _lf(lst):
    return lst + [e + 'f' for e in lst] + [e + 'l' for e in lst]


def _f(lst):
    return lst + [e + 'f' for e in lst]


exp_funcs = ['exp', 'exp2', 'expm1', 'log', 'log2', 'log10',
             'log1p', 'ilogb', 'logb']
power_funcs = ['sqrt', 'cbrt', 'hypot', 'pow']
trigonometric_funcs = ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'atan2']
hyperbolic_funcs = ['sinh', 'cosh', 'tanh', 'asinh', 'acosh', 'atanh']
nearest_funcs = ['ceil', 'floor', 'trunc', 'round', 'lround', 'llround',
                 'nearbyint', 'rint', 'lrint', 'llrint']
fp_funcs = ['frexp', 'ldexp', 'modf', 'scalbn', 'scalbln', 'nextafter',
            'nexttoward']
classification_funcs = ['fpclassify', 'isfinite', 'isinf', 'isnan',
                        'isnormal', 'signbit']

pymath_funcs = _f(['erf', 'erfc', 'lgamma', 'tgamma'])

fp_funcs = _lf([*exp_funcs, *power_funcs, *trigonometric_funcs,
                *hyperbolic_funcs, *nearest_funcs, *fp_funcs])

libm_funcs = [*fp_funcs, *classification_funcs]

stdio_funcs = ['printf', 'puts', 'fflush']

stdlib_funcs = ['free', 'calloc']


def get_function_dependencies(module, funcname, _deps=None):
    if _deps is None:
        _deps = dict()
    func = module.get_function(funcname)
    assert func.name == funcname, (func.name, funcname)
    for block in func.blocks:
        for instruction in block.instructions:
            if instruction.opcode == 'call':
                name = list(instruction.operands)[-1].name
                f = module.get_function(name)
                if name.startswith('llvm.'):
                    _deps[name] = 'intrinsic'
                elif f.is_declaration:
                    if name in libm_funcs:
                        _deps[name] = 'libm'
                    elif name in stdio_funcs:
                        _deps[name] = 'stdio'
                    elif name in stdlib_funcs:
                        _deps[name] = 'stdlib'
                    elif name in ['allocate_varlen_buffer']:
                        _deps[name] = 'omnisci_internal'
                    elif name in pymath_funcs:
                        _deps[name] = 'pymath'
                    else:
                        _deps[name] = 'undefined'
                else:
                    if name not in _deps:
                        _deps[name] = 'defined'
                        get_function_dependencies(module, name, _deps=_deps)
    return _deps


class JITRemoteCPUCodegen(codegen.JITCPUCodegen):
    # TODO: introduce JITRemoteCodeLibrary?
    _library_class = codegen.JITCodeLibrary

    def __init__(self, name, target_info):
        self.target_info = target_info
        super(JITRemoteCPUCodegen, self).__init__(name)

    def _get_host_cpu_name(self):
        return self.target_info.device_name

    def _get_host_cpu_features(self):
        features = self.target_info.device_features
        if llvm.llvm_version_info[0] < 9:
            # See https://github.com/xnd-project/rbc/issues/45
            for f in ['cx8', 'enqcmd', 'avx512bf16']:
                features = features.replace('+' + f, '').replace('-' + f, '')
        return features

    def _customize_tm_options(self, options):
        super(JITRemoteCPUCodegen, self)._customize_tm_options(options)
        # fix reloc_model as the base method sets it using local target
        if self.target_info.arch.startswith('x86'):
            reloc_model = 'static'
        else:
            reloc_model = 'default'
        options['reloc'] = reloc_model


class RemoteCPUContext(cpu.CPUContext):

    def __init__(self, typing_context, target_info):
        self.target_info = target_info
        super(RemoteCPUContext, self).__init__(typing_context)

    @compiler_lock.global_compiler_lock
    def init(self):
        self.address_size = self.target_info.bits
        self.is32bit = (self.address_size == 32)
        self._internal_codegen = JITRemoteCPUCodegen("numba.exec",
                                                     self.target_info)

        # Map external C functions.
        # nb.core.externals.c_math_functions.install(self)
        # TODO, seems problematic only for 32bit cases

        # Initialize NRT runtime
        # nb.core.argets.cpu.rtsys.initialize(self)
        # TODO: is this needed for LLVM IR generation?

        # import numba.unicode  # unicode support is not relevant here

    # TODO: overwrite load_additional_registries, call_conv?, post_lowering


def make_wrapper(fname, atypes, rtype, cres):
    """Make wrapper function to numba compile result.

    The compilation result contains a function with prototype::

      <status> <function name>(<rtype>** result, <arguments>)

    The make_wrapper adds a wrapper function to compilation result
    library with the following prototype::

      <rtype> <fname>(<arguments>)

    or, if <rtype> is Omnisci Array, then

      void <fname>(<rtype>* <arguments>)

    Parameters
    ----------
    fname : str
      Function name.
    atypes : tuple
      A tuple of argument Numba types.
    rtype : numba.Type
      The return Numba type
    cres : CompileResult
      Numba compilation result.

    """
    fndesc = cres.fndesc
    module = cres.library.create_ir_module(fndesc.unique_name)
    context = cres.target_context
    ll_argtypes = [context.get_value_type(ty) for ty in atypes]
    ll_return_type = context.get_value_type(rtype)

    # TODO: design a API for custom wrapping
    if type(rtype).__name__ == 'ArrayPointer':
        wrapty = ir.FunctionType(ir.VoidType(),
                                 [ll_return_type] + ll_argtypes)
        wrapfn = module.add_function(wrapty, fname)
        builder = ir.IRBuilder(wrapfn.append_basic_block('entry'))
        fnty = context.call_conv.get_function_type(rtype, atypes)
        fn = builder.module.add_function(fnty, cres.fndesc.llvm_func_name)
        status, out = context.call_conv.call_function(
            builder, fn, rtype, atypes, wrapfn.args[1:])
        with cgutils.if_unlikely(builder, status.is_error):
            cgutils.printf(builder,
                           f"rbc: {fname} failed with status code %i\n",
                           status.code)
            builder.ret_void()
        builder.store(builder.load(out), wrapfn.args[0])
        builder.ret_void()
    else:
        wrapty = ir.FunctionType(ll_return_type, ll_argtypes)
        wrapfn = module.add_function(wrapty, fname)
        builder = ir.IRBuilder(wrapfn.append_basic_block('entry'))
        fnty = context.call_conv.get_function_type(rtype, atypes)
        fn = builder.module.add_function(fnty, cres.fndesc.llvm_func_name)
        status, out = context.call_conv.call_function(
            builder, fn, rtype, atypes, wrapfn.args)
        with cgutils.if_unlikely(builder, status.is_error):
            cgutils.printf(builder,
                           f"rbc: {fname} failed with status code %i\n",
                           status.code)
        builder.ret(out)

    cres.library.add_ir_module(module)


def compile_to_LLVM(functions_and_signatures, target: TargetInfo,
                    pipeline_class=compiler.Compiler, debug=False):
    """Compile functions with given signatures to target specific LLVM IR.

    Parameters
    ----------
    functions_and_signatures : list
      Specify a list of Python function and its signatures pairs.
    target : TargetInfo
      Specify target device information.
    debug : bool

    Returns
    -------
    module : llvmlite.binding.ModuleRef
      LLVM module instance. To get the IR string, use `str(module)`.

    """
    target_desc = registry.cpu_target
    if target is None:
        target = TargetInfo.host()
        typing_context = target_desc.typing_context
        target_context = target_desc.target_context
    else:
        typing_context = typing.Context()
        target_context = RemoteCPUContext(typing_context, target)
        # Bring over Array overloads (a hack):
        target_context._defns = target_desc.target_context._defns
        # Fixes rbc issue 74:
        target_desc.typing_context.target_info = target
        target_desc.target_context.target_info = target

    typing_context.target_info = target
    target_context.target_info = target

    codegen = target_context.codegen()
    main_library = codegen.create_library('rbc.irtools.compile_to_IR')
    main_module = main_library._final_module

    flags = compiler.Flags()
    flags.set('no_compile')
    flags.set('no_cpython_wrapper')
    if get_version('numba') >= (0, 49):
        flags.set('no_cfunc_wrapper')

    function_names = []
    for func, signatures in functions_and_signatures:
        for sig in signatures:
            fname = func.__name__ + sig.mangling()
            function_names.append(fname)
            args, return_type = sigutils.normalize_signature(
                sig.tonumba(bool_is_int8=True))
            cres = compiler.compile_extra(typingctx=typing_context,
                                          targetctx=target_context,
                                          func=func,
                                          args=args,
                                          return_type=return_type,
                                          flags=flags,
                                          library=main_library,
                                          locals={},
                                          pipeline_class=pipeline_class)
            make_wrapper(fname, args, return_type, cres)

    seen = set()
    for _library in main_library._linking_libraries:
        if _library not in seen:
            seen.add(_library)
            main_module.link_in(
                _library._get_module_for_linking(), preserve=True,
            )

    main_library._optimize_final_module()

    # Catch undefined functions:
    used_functions = set(function_names)
    for fname in function_names:
        deps = get_function_dependencies(main_module, fname)
        for fn, descr in deps.items():
            used_functions.add(fn)
            if descr == 'undefined':
                if fn.startswith('numba_') and target.has_numba:
                    continue
                if fn.startswith('Py') and target.has_cpython:
                    continue
                raise RuntimeError('function `%s` is undefined' % (fn))

    # for global_variable in main_module.global_variables:
    #    global_variable.linkage = llvm.Linkage.private

    unused_functions = [f.name for f in main_module.functions
                        if f.name not in used_functions]

    if debug:
        print('compile_to_IR: the following functions are used')
        for fname in used_functions:
            lf = main_module.get_function(fname)
            print('  [ALIVE]', fname, 'with', lf.linkage)

    if unused_functions:
        if debug:
            print('compile_to_IR: the following functions are not used'
                  ' and will be removed:')
        for fname in unused_functions:
            lf = main_module.get_function(fname)
            if lf.is_declaration:
                # if the function is a declaration,
                # we just put the linkage as external
                lf.linkage = llvm.Linkage.external
            else:
                # but if the function is not a declaration,
                # we change the linkage to private
                lf.linkage = llvm.Linkage.private
            if debug:
                print('  [DEAD]', fname, 'with', lf.linkage)

        main_library._optimize_final_module()
    # TODO: determine unused global_variables and struct_types

    main_module.verify()
    main_library._finalized = True

    main_module.triple = target.triple
    main_module.data_layout = target.datalayout

    return main_module


def compile_IR(ir):
    """Return execution engine with IR compiled in.

    Parameters
    ----------
    ir : str
      Specify LLVM IR code as a string.

    Returns
    -------
    engine :
      Execution engine.


    Examples
    --------

        To get the address of the compiled functions, use::

          addr = engine.get_function_address("<function name>")
    """
    triple = re.search(
        r'target\s+triple\s*=\s*"(?P<triple>[-\d\w\W_]+)"\s*$',
        ir, re.M).group('triple')

    # Create execution engine
    target = llvm.Target.from_triple(triple)
    target_machine = target.create_target_machine()
    backing_mod = llvm.parse_assembly("")
    engine = llvm.create_mcjit_compiler(backing_mod, target_machine)

    # Create LLVM module and compile
    mod = llvm.parse_assembly(ir)
    mod.verify()
    engine.add_module(mod)
    engine.finalize_object()
    engine.run_static_constructors()

    return engine


def cg_fflush(builder):
    int8_t = ir.IntType(8)
    fflush_fnty = ir.FunctionType(int32_t, [int8_t.as_pointer()])
    fflush_fn = builder.module.get_or_insert_function(
        fflush_fnty, name='fflush')

    builder.call(fflush_fn, [int8_t.as_pointer()(None)])


@extending.intrinsic
def fflush(typingctx):
    """fflush that can be called from Numba jit-decorated functions.
    """
    sig = nb_types.void(nb_types.void)

    def codegen(context, builder, signature, args):
        cg_fflush(builder)

    return sig, codegen


@extending.intrinsic
def printf(typingctx, format_type, *args):
    """printf that can be called from Numba jit-decorated functions.
    """
    if isinstance(format_type, nb_types.StringLiteral):
        sig = nb_types.void(format_type, nb_types.BaseTuple.from_types(args))

        def codegen(context, builder, signature, args):
            cgutils.printf(builder, format_type.literal_value, *args[1:])
            cg_fflush(builder)

        return sig, codegen
