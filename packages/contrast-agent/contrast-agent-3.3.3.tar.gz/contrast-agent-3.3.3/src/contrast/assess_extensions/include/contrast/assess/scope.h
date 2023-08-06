/*
* Copyright © 2020 Contrast Security, Inc.
* See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
*/
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>


#define CONTRAST_SCOPE      0
#define PROPAGATION_SCOPE   1
#define TRIGGER_SCOPE       2


PyObject *enter_scope(PyObject *self, PyObject *args);
PyObject *exit_scope(PyObject *self, PyObject *args);
PyObject *in_scope(PyObject *self, PyObject *args);
PyObject *set_thread_scope(PyObject *self, PyObject *thread_id);
PyObject *destroy_thread_scope(PyObject *self, PyObject *thread_id);
PyObject *get_thread_scope(PyObject *self, PyObject *args);

void enter_contrast_scope(void);
void exit_contrast_scope(void);
void enter_propagation_scope(void);
void exit_propagation_scope(void);
int should_propagate(void);
