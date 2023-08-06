from _ase_ext import ffi


def doublep(array):
    assert array.dtype == float
    return ffi.cast('double*', ffi.from_buffer(array))


def longp(array):
    assert array.dtype == int
    return ffi.cast('long*', ffi.from_buffer(array))
