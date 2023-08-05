/*
* Copyright © 2020 Contrast Security, Inc.
* See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
*/
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <pthread.h>

#include <contrast/assess/scope.h>
#include <contrast/assess/logging.h>


typedef struct thread_scope {
    int contrast_scope;
    int propagation_scope;
    int trigger_scope;
} thread_scope_t;


static pthread_key_t thread_key;
static pthread_once_t once_key = PTHREAD_ONCE_INIT;
/* Forward declaration */
static thread_scope_t *get_scope(void);


inline void enter_contrast_scope(void) {
    thread_scope_t *scope;

    if ((scope = get_scope()) == NULL)
        return;

    scope->contrast_scope++;
}


inline void exit_contrast_scope(void) {
    thread_scope_t *scope;

    if ((scope = get_scope()) == NULL)
        return;


    if (scope->contrast_scope > 0)
        scope->contrast_scope--;
}


inline void enter_propagation_scope(void) {
    thread_scope_t *scope;

    if ((scope = get_scope()) == NULL)
        return;

    scope->propagation_scope++;
}


inline void exit_propagation_scope(void) {
    thread_scope_t *scope;

    if ((scope = get_scope()) == NULL)
        return;

    if (scope->propagation_scope > 0)
        scope->propagation_scope--;
}


inline int should_propagate(void) {
    thread_scope_t *scope = get_scope();

    if (scope == NULL) {
        return 0;
    }

    return !(scope->contrast_scope || scope->propagation_scope || scope->trigger_scope);
}


PyObject *enter_scope(PyObject *self, PyObject *args) {
    int scope_id;
    thread_scope_t *scope;

    if ((scope = get_scope()) == NULL) {
        PyErr_Format(PyExc_RuntimeError, "Failed to get scope state for this thread");
        return NULL;
    }

    if (!PyArg_ParseTuple(args, "i", &scope_id))
        return NULL;

    if (scope_id == CONTRAST_SCOPE)
        scope->contrast_scope++;
    else if (scope_id == PROPAGATION_SCOPE)
        scope->propagation_scope++;
    else if (scope_id == TRIGGER_SCOPE)
        scope->trigger_scope++;

    Py_RETURN_NONE;
}


PyObject *exit_scope(PyObject *self, PyObject *args) {
    int scope_id;
    thread_scope_t *scope;

    if ((scope = get_scope()) == NULL) {
        PyErr_Format(PyExc_RuntimeError, "Failed to get scope state for this thread");
        return NULL;
    }

    if (!PyArg_ParseTuple(args, "i", &scope_id))
        return NULL;

    if (scope_id == CONTRAST_SCOPE && scope->contrast_scope > 0)
        scope->contrast_scope--;
    else if (scope_id == PROPAGATION_SCOPE && scope->propagation_scope > 0)
        scope->propagation_scope--;
    else if (scope_id == TRIGGER_SCOPE && scope->trigger_scope > 0)
        scope->trigger_scope--;

    Py_RETURN_NONE;
}


PyObject *in_scope(PyObject *self, PyObject *args) {
    int scope_id;
    thread_scope_t *scope;

    if ((scope = get_scope()) == NULL) {
        PyErr_Format(PyExc_RuntimeError, "Failed to get scope state for this thread");
        return NULL;
    }

    if (!PyArg_ParseTuple(args, "i", &scope_id))
        return NULL;

    if (scope_id == CONTRAST_SCOPE)
        return PyBool_FromLong(scope->contrast_scope);
    else if (scope_id == PROPAGATION_SCOPE)
        return PyBool_FromLong(scope->propagation_scope);
    else if (scope_id == TRIGGER_SCOPE)
        return PyBool_FromLong(scope->trigger_scope);

    Py_RETURN_FALSE;
}


static void init_thread_key(void) {
    (void) pthread_key_create(&thread_key, NULL);
}


static int init_thread_scope(const thread_scope_t *scope_level) {
    thread_scope_t *scope;

    /* This guarantees that initialization will only happen once per process */
    pthread_once(&once_key, init_thread_key);

    /* Thread scope has already been initialized, so do nothing */
    if (pthread_getspecific(thread_key) != NULL)
        return 1;

    log_debug("init thread scope");

    if ((scope = malloc(sizeof(*scope))) == NULL) {
        log_error("Failed to allocate scope for thread");
        return 0;
    }

    memcpy(scope, scope_level, sizeof(*scope));

    pthread_setspecific(thread_key, scope);

    return 1;
}


PyObject *set_thread_scope(PyObject *self, PyObject *py_scope) {
    /* Parse scope out of tuple */
    thread_scope_t scope;

    if (!PyArg_ParseTuple(
            py_scope,
            "iii",
            &scope.contrast_scope,
            &scope.propagation_scope,
            &scope.trigger_scope)) {
        PyErr_Format(PyExc_RuntimeError, "Failed to parse scope from tuple");
        return NULL;
    }

    /* Initialize scope if this is being called for the first time */
    if (!init_thread_scope(&scope)) {
        PyErr_Format(PyExc_RuntimeError, "Failed to allocate scope for thread");
        return NULL;
    }

    Py_RETURN_NONE;
}


static thread_scope_t *get_scope() {
    static const thread_scope_t zero_scope;
    thread_scope_t *scope;

    /* If scope is not initialized for this thread at the time this is called, it
     * indicates that we are in a thread that existed before we added instrumentation.
     * This means that there was no scope, so we just initialize with zero scope.
     */
    if (!init_thread_scope(&zero_scope)) {
        log_error("Failed to initialize thread scope");
        return NULL;
    }

    if ((scope = pthread_getspecific(thread_key)) == NULL) {
        log_error("Failed to retrieve scope for thread");
        return NULL;
    }

    return scope;
}


PyObject *get_thread_scope(PyObject *self, PyObject *args) {
    thread_scope_t *scope;

    if ((scope = get_scope()) == NULL) {
        PyErr_Format(PyExc_RuntimeError, "Failed to get scope state for this thread");
        return NULL;
    }

    return Py_BuildValue(
        "(iii)",
        scope->contrast_scope,
        scope->propagation_scope,
        scope->trigger_scope
    );
}


PyObject *destroy_thread_scope(PyObject *self, PyObject *thread_id) {
    thread_scope_t *scope;

    log_debug("destroy thread scope");

    scope = pthread_getspecific(thread_key);
    if (scope != NULL)
        free(scope);

    Py_RETURN_NONE;
}
