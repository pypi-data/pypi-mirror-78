/*
* Copyright © 2020 Contrast Security, Inc.
* See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
*/
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <contrast/assess/patches.h>
#include <contrast/assess/scope.h>


static PyMethodDef methods[] = {
    {"enable", (PyCFunction)enable, METH_VARARGS|METH_KEYWORDS, "Patch relevant string functions"},
    {"disable", disable, METH_O, "Remove all patches"},
    {"enter_scope", enter_scope, METH_VARARGS, "Enter given scope"},
    {"exit_scope", exit_scope, METH_VARARGS, "Exit given scope"},
    {"in_scope", in_scope, METH_VARARGS, "Check whether in given scope"},
    {"set_thread_scope", set_thread_scope, METH_O, "Set scope level for new thread"},
    {"destroy_thread_scope", destroy_thread_scope, METH_NOARGS, "Teardown scope for thread"},
    {"get_thread_scope", get_thread_scope, METH_NOARGS, "Get scope level for thread"},
    {"set_attr_on_type", set_attr_on_type, METH_VARARGS, "Set attribute on type"},
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef cs_str_definition = {
    PyModuleDef_HEAD_INIT,
    "cs_str",
    "description here",
    -1,
    methods,
    NULL,
    NULL,
    NULL,
    NULL
};


PyMODINIT_FUNC PyInit_cs_str(void) {
    PyObject *module;

    Py_Initialize();
    module = PyModule_Create(&cs_str_definition);
    PyModule_AddIntConstant(module, "CONTRAST_SCOPE", CONTRAST_SCOPE);
    PyModule_AddIntConstant(module, "PROPAGATION_SCOPE", PROPAGATION_SCOPE);
    PyModule_AddIntConstant(module, "TRIGGER_SCOPE", TRIGGER_SCOPE);

    return module;
}
