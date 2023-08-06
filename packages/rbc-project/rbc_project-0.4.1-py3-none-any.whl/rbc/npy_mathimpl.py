import math
import numpy as np
from numba.extending import register_jitable
from llvmlite import ir
from .utils import get_version
if get_version('numba') >= (0, 49):
    from numba.cpython import mathimpl
    from numba.np import ufunc_db
else:
    from numba.targets import mathimpl, ufunc_db

# tell numba to wire np.exp2 to libm exp2.
mathimpl.unary_math_extern(np.exp2, "exp2f", "exp2")
mathimpl.unary_math_extern(np.log2, "log2f", "log2")
mathimpl.unary_math_extern(math.gamma, "tgammaf", "tgamma")


def np_logaddexp_impl(context, builder, sig, args):
    # based on NumPy impl.
    # https://github.com/numpy/numpy/blob/30f985499b77381ab4748692cc76c55048ca0548/numpy/core/src/npymath/npy_math_internal.h.src#L585-L604
    def impl(x, y):
        if x == y:
            LOGE2 = 0.693147180559945309417232121458176568  # log_e 2
            return x + LOGE2
        else:
            tmp = x - y
            if tmp > 0:
                return x + np.log1p(np.exp(-tmp))
            elif tmp <= 0:
                return y + np.log1p(np.exp(tmp))
            else:
                # NaN's
                return tmp

    return context.compile_internal(builder, impl, sig, args)


@register_jitable
def log2_1p(x):
    LOG2E = 1.442695040888963407359924681001892137  # log_2 e
    return LOG2E * np.log1p(x)


def impl(x, y):
    if x == y:
        return x + 1
    else:
        tmp = x - y
        if tmp > 0:
            return x + log2_1p(np.exp2(-tmp))
        elif tmp <= 0:
            return y + log2_1p(np.exp2(tmp))
        else:
            # NaN's
            return tmp


def np_logaddexp2_impl(context, builder, sig, args):

    def impl(x, y):
        if x == y:
            return x + 1
        else:
            tmp = x - y
            if tmp > 0:
                return x + log2_1p(np.exp2(-tmp))
            elif tmp <= 0:
                return y + log2_1p(np.exp2(tmp))
            else:
                # NaN's
                return tmp

    return context.compile_internal(builder, impl, sig, args)


def np_signbit_impl(context, builder, sig, args):
    int64_t = ir.IntType(64)
    double = ir.DoubleType()
    [val] = args
    val = builder.bitcast(builder.fpext(val, double), int64_t)
    res = builder.ashr(val, int64_t(63))
    return res


def np_ldexp_impl(context, builder, sig, args):

    def impl(x1, x2):
        if x2 < 0:
            return x1 / np.power(2, -x2)
        return x1 * np.power(2, x2)

    return context.compile_internal(builder, impl, sig, args)


ufunc_db._lazy_init_db()

# logaddexp
ufunc_db._ufunc_db[np.logaddexp] = {
    'ff->f': np_logaddexp_impl,
    'dd->d': np_logaddexp_impl,
}

# logaddexp2
ufunc_db._ufunc_db[np.logaddexp2] = {
    'ff->f': np_logaddexp2_impl,
    'dd->d': np_logaddexp2_impl,
}

# signbit
ufunc_db._ufunc_db[np.signbit] = {
    'f->?': np_signbit_impl,
    'd->?': np_signbit_impl,
}

ufunc_db._ufunc_db[np.ldexp] = {
    'fi->f': np_ldexp_impl,
    'fl->f': np_ldexp_impl,
    'di->d': np_ldexp_impl,
    'dl->d': np_ldexp_impl,
}
