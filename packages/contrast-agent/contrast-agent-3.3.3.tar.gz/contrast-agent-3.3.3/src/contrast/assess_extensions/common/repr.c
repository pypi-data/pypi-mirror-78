/*
* Copyright © 2020 Contrast Security, Inc.
* See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
*/
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <funchook.h>

#include <contrast/assess/propagate.h>
#include <contrast/assess/utils.h>


unaryfunc bytes_repr_orig;
unaryfunc unicode_repr_orig;
unaryfunc bytearray_repr_orig;
HOOK_UNARYFUNC(bytes_repr, "__repr__");
HOOK_UNARYFUNC(unicode_repr, "__repr__");
HOOK_UNARYFUNC(bytearray_repr, "__repr__");


int apply_repr_patches(funchook_t *funchook) {
    bytes_repr_orig = PyBytes_Type.tp_repr;
    unicode_repr_orig = PyUnicode_Type.tp_repr;
    bytearray_repr_orig = PyByteArray_Type.tp_repr;

    funchook_prep_wrapper(funchook, &bytes_repr_orig, bytes_repr_new);
    funchook_prep_wrapper(funchook, &unicode_repr_orig, unicode_repr_new);
    funchook_prep_wrapper(funchook, &bytearray_repr_orig, bytearray_repr_new);

    return 0;
}
