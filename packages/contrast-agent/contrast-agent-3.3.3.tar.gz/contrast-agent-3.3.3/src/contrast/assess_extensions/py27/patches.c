/*
* Copyright © 2020 Contrast Security, Inc.
* See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
*/
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <contrast/assess/patches.h>
#include <contrast/assess/scope.h>


/* This function is used for building a map between str and unicode objects and
 * their underlying char * buffers. This enables us to do a reverse lookup
 * based on char * pointers from the hooked exec statement.
 */
static PyObject *get_str_pointer(PyObject *self, PyObject *str) {
    unsigned long ptr_val;

    if (!PyString_Check(str))
        Py_RETURN_NONE;

    /* Get the pointer to the underlying string as an integer value */
    ptr_val = (unsigned long) PyString_AS_STRING(str);
    return PyLong_FromUnsignedLong(ptr_val);
}


static PyMethodDef methods[] = {
    {"enable", (PyCFunction)enable, METH_VARARGS|METH_KEYWORDS, "Patch relevant string functions"},
    {"disable", disable, METH_O, "Remove all patches"},
    {"enter_scope", enter_scope, METH_VARARGS, "Enter given scope"},
    {"exit_scope", exit_scope, METH_VARARGS, "Exit given scope"},
    {"in_scope", in_scope, METH_VARARGS, "Check whether in given scope"},
    {"set_thread_scope", set_thread_scope, METH_O, "Set scope level for new thread"},
    {"get_thread_scope", get_thread_scope, METH_NOARGS, "Get scope level for thread"},
    {"destroy_thread_scope", destroy_thread_scope, METH_NOARGS, "Teardown scope for thread"},
    {"set_attr_on_type", set_attr_on_type, METH_VARARGS, "Set attribute on type"},
    {"get_str_pointer", get_str_pointer, METH_O, "Get pointer to underlying string"},
};


PyMODINIT_FUNC initcs_str(void) {
    PyObject *module = Py_InitModule("cs_str", methods);
    PyModule_AddIntConstant(module, "CONTRAST_SCOPE", CONTRAST_SCOPE);
    PyModule_AddIntConstant(module, "PROPAGATION_SCOPE", PROPAGATION_SCOPE);
    PyModule_AddIntConstant(module, "TRIGGER_SCOPE", TRIGGER_SCOPE);
}
