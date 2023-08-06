/*
* Copyright © 2020 Contrast Security, Inc.
* See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
*/
#ifndef _ASSESS_UTILS_H_
#define _ASSESS_UTILS_H_
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <funchook.h>

#include <contrast/assess/logging.h>


typedef PyObject *(*fastcall_method)(PyObject *, PyObject *const *, Py_ssize_t);
typedef PyObject *(*ternary_fastcall_method)(PyObject *, PyObject *const *, Py_ssize_t, PyObject *);


static inline PyObject *pack_args_tuple(PyObject *const *args, Py_ssize_t nargs) {
    PyObject *hook_args = PyList_New(0);
    Py_ssize_t i;

    for (i = 0; i < nargs; i++) {
        PyList_Append(hook_args, args[i]);
    }

    return hook_args;
}


static inline PyObject *pack_kwargs_dict(PyObject *const *args,
                                         Py_ssize_t nargs, PyObject *kwnames) {
    PyObject *kwargs = PyDict_New();
    PyObject *name;
    Py_ssize_t i;

    if (kwnames == NULL)
        goto cleanup_and_exit;

    for (i = 0; i < PySequence_Size(kwnames); i++) {
        name = PySequence_GetItem(kwnames, i);
        PyDict_SetItem(kwargs, name, args[i + nargs]);
        Py_DECREF(name);
    }

cleanup_and_exit:
    return kwargs;
}


#define funchook_prep_wrapper(fh, oldf, newf)                               \
    do {                                                                    \
        if (funchook_prepare((fh), (void **)(oldf), (void *)(newf)) != FUNCHOOK_ERROR_SUCCESS)\
        {                                                                   \
            log_exception(                                                  \
                PyExc_RuntimeError,                                         \
                "failed to prepare hook at %s:%d: %s",                      \
                __FILE__,                                                   \
                __LINE__,                                                   \
                funchook_error_message(fh));                                \
            return -1;                                                      \
        }                                                                   \
    } while (0)


#define HOOK_UNARYFUNC(NAME, EVENT)                                 \
    static PyObject *NAME##_new(PyObject *self) {                   \
        PyObject *result = NAME##_orig(self);                       \
                                                                    \
        if (result == NULL)                                         \
            return result;                                          \
                                                                    \
        propagate_result(EVENT, self, result, NULL, NULL);          \
                                                                    \
        return result;                                              \
    }


#define HOOK_BINARYFUNC(NAME, EVENT)                                \
    static PyObject *NAME##_new(PyObject *self, PyObject *args) {   \
        PyObject *result = NAME##_orig(self, args);                 \
                                                                    \
        if (result == NULL)                                         \
            return result;                                          \
                                                                    \
        propagate_result(EVENT, self, result, args, NULL);          \
                                                                    \
        return result;                                              \
    }


#define HOOK_TERNARYFUNC(NAME, EVENT)                               \
    static PyObject *NAME##_new(PyObject *self, PyObject *args,     \
                                PyObject *kwds) {                   \
        PyObject *result = NAME##_orig(self, args, kwds);           \
                                                                    \
        if (result == NULL)                                         \
            return result;                                          \
                                                                    \
        propagate_result(EVENT, self, result, args, kwds);          \
                                                                    \
        return result;                                              \
    }


#define HOOK_FASTCALL(NAME, EVENT)                                      \
    static PyObject *NAME##_new(PyObject *self, PyObject *const *args,  \
                                Py_ssize_t nargs) {                     \
        PyObject *hook_args = pack_args_tuple(args, nargs);             \
        PyObject *result = NAME##_orig(self, args, nargs);              \
                                                                        \
        if (result == NULL)                                             \
            goto cleanup_and_exit;                                      \
                                                                        \
        propagate_result(EVENT, self, result, hook_args, NULL);         \
                                                                        \
cleanup_and_exit:                                                       \
        Py_XDECREF(hook_args);                                          \
        return result;                                                  \
    }


#define HOOK_TERNARY_FASTCALL(NAME, EVENT)                              \
    static PyObject *NAME##_new(PyObject *self, PyObject *const *args,  \
                                Py_ssize_t nargs, PyObject *kwnames) {  \
        PyObject *hook_args = pack_args_tuple(args, nargs);             \
        PyObject *result = NAME##_orig(self, args, nargs, kwnames);     \
                                                                        \
        if (result == NULL)                                             \
            goto cleanup_and_exit;                                      \
                                                                        \
        propagate_result(EVENT, self, result, hook_args, NULL);         \
                                                                        \
cleanup_and_exit:                                                       \
        Py_XDECREF(hook_args);                                          \
        return result;                                                  \
    }


#define HOOK_STREAM_UNARYFUNC(NAME, EVENT)                          \
    static PyObject *NAME##_new(PyObject *self) {                   \
        PyObject *result = NAME##_orig(self);                       \
                                                                    \
        if (result == NULL)                                         \
            return result;                                          \
                                                                    \
        propagate_stream(EVENT, self, result, NULL, NULL);          \
                                                                    \
        return result;                                              \
    }


#define HOOK_STREAM_BINARYFUNC(NAME, EVENT)                             \
    static PyObject *NAME##_new(PyObject *self, PyObject *args) {       \
        PyObject *result = NAME##_orig(self, args);                     \
                                                                        \
        if (result == NULL)                                             \
            return result;                                              \
                                                                        \
        propagate_stream(EVENT, self, result, args, NULL);              \
                                                                        \
        return result;                                                  \
    }


#define HOOK_STREAM_FASTCALL(NAME, EVENT)                               \
PyObject *NAME##_new(PyObject *self, PyObject *const *args,             \
                     Py_ssize_t nargs) {                                \
    PyObject *hook_args = pack_args_tuple(args, nargs);                 \
    if (hook_args == NULL)                                              \
        PyErr_Clear();                                                  \
                                                                        \
    PyObject *result = NAME##_orig(self, args, nargs);                  \
                                                                        \
    if (result == NULL || hook_args == NULL)                            \
        goto cleanup_and_exit;                                          \
                                                                        \
    propagate_stream(EVENT, self, result, hook_args, NULL);             \
                                                                        \
cleanup_and_exit:                                                       \
    Py_XDECREF(hook_args);                                              \
    return result;                                                      \
}


#define ADD_METHOD_HOOK(TYPE, NAME, OFFSET)                                 \
    NAME##_orig = (void *)TYPE.tp_methods[OFFSET].ml_meth;                  \
    funchook_prep_wrapper(funchook, (PyCFunction)&NAME##_orig, NAME##_new);


#define ADD_STREAM_HOOK(TYPE, NAME, OFFSET)                                 \
    NAME##_orig = (void *)TYPE->tp_methods[OFFSET].ml_meth;                 \
    funchook_prep_wrapper(funchook, (PyCFunction)&NAME##_orig, NAME##_new);


#define ADD_NEWFUNC_HOOK(TYPE, NAME)                                        \
    NAME##_orig = (void *)TYPE.tp_new;                                      \
    funchook_prep_wrapper(funchook, (PyCFunction)&NAME##_orig, NAME##_new);


#define ADD_INITPROC_HOOK(TYPE, NAME)                                        \
    NAME##_orig = (void *)TYPE.tp_init;                                      \
    funchook_prep_wrapper(funchook, (PyCFunction)&NAME##_orig, NAME##_new);


/* For convenience/brevity */
#define ADD_BYTEARRAY_HOOK(X, Y)    ADD_METHOD_HOOK(PyByteArray_Type, X, Y)


#endif /* _ASSESS_UTILS_H_ */
