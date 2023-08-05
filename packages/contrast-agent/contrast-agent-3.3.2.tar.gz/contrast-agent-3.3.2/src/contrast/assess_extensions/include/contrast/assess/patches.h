/*
* Copyright © 2020 Contrast Security, Inc.
* See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
*/
#ifndef _ASSESS_PATCHES_H_
#define _ASSESS_PATCHES_H_
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <funchook.h>


PyObject *enable(PyObject *self, PyObject *args, PyObject *kwargs);
PyObject *disable(PyObject *self, PyObject *args);
PyObject *set_attr_on_type(PyObject *self, PyObject *args);

int apply_cat_patch(funchook_t *funchook);
int apply_subscript_patch(funchook_t *funchook);
int apply_format_patch(funchook_t *funchook);
int apply_unicode_patches(funchook_t *funchook);
int apply_bytes_patches(funchook_t *funchook);
int apply_bytearray_patches(funchook_t *funchook);
int apply_stream_patches(funchook_t *funchook);
int apply_repr_patches(funchook_t *funchook);
#if PY_MAJOR_VERSION < 3
int apply_exec_patches(funchook_t *funchook);
#endif
int patch_stringio_methods(funchook_t *funchook, PyTypeObject *StreamType);
int patch_bytesio_methods(funchook_t *funchook, PyTypeObject *StreamType);
int patch_iobase_methods(funchook_t *funchook, PyTypeObject *StreamType);


#endif /* _ASSESS_PATCHES_H_ */
