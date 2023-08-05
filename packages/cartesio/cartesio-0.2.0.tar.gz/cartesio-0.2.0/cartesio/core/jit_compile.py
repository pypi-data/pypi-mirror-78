import os
import warnings
from functools import wraps

__all__ = ["jit_compile"]

ENV_CARTESIO_DISABLE_JIT_COMPILE = "CARTESIO_DISABLE_JIT_COMPILE"
DISABLE_JIT_COMPILE = os.getenv(ENV_CARTESIO_DISABLE_JIT_COMPILE, "FALSE").upper() in {
    "TRUE",
    "YES",
    "1",
}

_numba_jit_compile = False
if not DISABLE_JIT_COMPILE:
    try:
        import numba

        jit_compile = numba.njit

        _numba_jit_compile = True

    except ModuleNotFoundError:

        warnings.warn("Numba module not found. Performance will be degraded")
else:
    warnings.warn(
        "Numba jit compilation disabled via environment variable {}. "
        "Performance will be degraded".format(ENV_CARTESIO_DISABLE_JIT_COMPILE)
    )

if _numba_jit_compile is False:

    def jit_compile(py_signature_or_function=None, **numba_kwargs):
        if py_signature_or_function is None:

            def decorator(py_signature_or_function_inner):

                if not hasattr(py_signature_or_function_inner, "py_func"):
                    setattr(
                        py_signature_or_function_inner,
                        "py_func",
                        py_signature_or_function_inner,
                    )

                @wraps(py_signature_or_function_inner)
                def inner(*args, **kwargs):
                    return py_signature_or_function_inner(*args, **kwargs)

                return inner

            return decorator
        else:

            if not hasattr(py_signature_or_function, "py_func"):
                setattr(py_signature_or_function, "py_func", py_signature_or_function)
            return py_signature_or_function
