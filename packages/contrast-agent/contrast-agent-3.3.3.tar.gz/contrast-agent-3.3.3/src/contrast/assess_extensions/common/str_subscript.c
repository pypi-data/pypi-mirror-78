/*
* Copyright © 2020 Contrast Security, Inc.
* See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
*/
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <assert.h>
#include <ctype.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>

#include <funchook.h>

#include <contrast/assess/patches.h>
#include <contrast/assess/propagate.h>
#include <contrast/assess/scope.h>
#include <contrast/assess/utils.h>

/*
* Subscript:
*
* Returns a slice of a string
*
* Source: Origin/Self
* Target: Return
* Action: Keep
*/

#if PY_MAJOR_VERSION < 3
#define PY2
#endif /* PY_MAJOR_VERSION < 3 */


#define HOOK_SUBSCRIPT(NAME)                                        \
    PyObject *NAME##_new(PyObject *a, PyObject *b) {                \
        PyObject *result;                                           \
                                                                    \
        enter_propagation_scope();                                  \
        result = NAME##_orig(a, b);                                 \
        exit_propagation_scope();                                   \
                                                                    \
        PyObject *args = PyTuple_Pack(1, b);                        \
                                                                    \
        /* Record input and result */                               \
        if (result != NULL && !PyNumber_Check(result))              \
            propagate_result("subscript", a, result, args, NULL);   \
                                                                    \
        Py_XDECREF(args);                                           \
        return result;                                              \
    }


#define HOOK_SLICE(NAME)                                                    \
    PyObject *NAME##_new(PyObject *a, Py_ssize_t i1, Py_ssize_t i2) {       \
        PyObject *result;                                                   \
                                                                            \
        enter_contrast_scope();                                             \
        result = NAME##_orig(a, i1, i2);                                    \
        exit_contrast_scope();                                              \
                                                                            \
        PyObject *slice = build_slice(a, i1, i2);                           \
                                                                            \
        PyObject *args = PyTuple_Pack(1, slice);                            \
                                                                            \
        /* Record input and result */                                       \
        if (result != NULL)                                                 \
            propagate_result("subscript", a, result, args, NULL);           \
                                                                            \
        Py_XDECREF(slice);                                                  \
        Py_XDECREF(args);                                                   \
                                                                            \
        return result;                                                      \
    }


#ifdef PY2
static inline PyObject *build_slice(PyObject *a, Py_ssize_t i, Py_ssize_t j) {
    /* Copied from string_slice in Objects/stringobject.c in Py2.7 */
    if (i < 0)
        i = 0;
    if (j < 0)
        j = 0; /* Avoid signed/unsigned bug in next line */
    if (j > Py_SIZE(a))
        j = Py_SIZE(a);
    if (j < i)
        j = i;

    PyObject *start = PyInt_FromSsize_t(i);
    PyObject *stop = PyInt_FromSsize_t(j);

    PyObject *slice = PySlice_New(start, stop, NULL);

    Py_XDECREF(start);
    Py_XDECREF(stop);

    return slice;
}
#endif /* ifdef PY2 */


binaryfunc unicode_item_orig;
binaryfunc bytearray_item_orig;
HOOK_SUBSCRIPT(unicode_item);
HOOK_SUBSCRIPT(bytearray_item);

#ifdef PY2
binaryfunc string_item_orig;
ssizessizeargfunc unicode_slice_orig;
ssizessizeargfunc string_slice_orig;
HOOK_SUBSCRIPT(string_item);
HOOK_SLICE(unicode_slice);
HOOK_SLICE(string_slice);


#ifdef UBUNTU_XENIAL
ssizessizeargfunc seq_slice_orig;
PyObject *seq_slice_new(PyObject *a, Py_ssize_t i1, Py_ssize_t i2) {
    PyObject *result;

    enter_contrast_scope();
    result = seq_slice_orig(a, i1, i2);
    exit_contrast_scope();

    /* We're hooking this because we need it as a string propagator, but it gets called
     * with other types as well. We want to gate our propagation logic so that we don't
     * hurt performance and/or create extraenous events.
     */
    if (!(PyUnicode_Check(a) || PyByteArray_Check(a) || PyString_Check(a)))
        return result;

    PyObject *slice = build_slice(a, i1, i2);

    PyObject *args = PyTuple_Pack(1, slice);

    /* Record input and result */
    if (result != NULL)
        propagate_result("subscript", a, result, args, NULL);

    Py_XDECREF(slice);
    Py_XDECREF(args);

    return result;
}
#endif /* UBUNTU_XENIAL */


#else
binaryfunc bytes_item_orig;
HOOK_SUBSCRIPT(bytes_item);
#endif /* ifdef PY2 */


/* apply our patches */
int apply_subscript_patch(funchook_t *funchook) {
#ifdef PY2
    string_item_orig = PyString_Type.tp_as_mapping->mp_subscript;
    string_slice_orig = PyString_Type.tp_as_sequence->sq_slice;
    unicode_slice_orig = PyUnicode_Type.tp_as_sequence->sq_slice;

    funchook_prep_wrapper(funchook, &string_item_orig, string_item_new);
    funchook_prep_wrapper(funchook, &string_slice_orig, string_slice_new);
    funchook_prep_wrapper(funchook, &unicode_slice_orig, unicode_slice_new);

#ifdef UBUNTU_XENIAL
    seq_slice_orig = PySequence_GetSlice;
    funchook_prep_wrapper(funchook, &seq_slice_orig, seq_slice_new);
#endif /* UBUNTU_XENIAL */

#else
    bytes_item_orig = PyBytes_Type.tp_as_mapping->mp_subscript;
    funchook_prep_wrapper(funchook, &bytes_item_orig, bytes_item_new);
#endif /* ifdef PY2 */

    unicode_item_orig = PyUnicode_Type.tp_as_mapping->mp_subscript;
    funchook_prep_wrapper(funchook, &unicode_item_orig, unicode_item_new);

    bytearray_item_orig = PyByteArray_Type.tp_as_mapping->mp_subscript;
    funchook_prep_wrapper(funchook, &bytearray_item_orig, bytearray_item_new);

    return 0;
}
