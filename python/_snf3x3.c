#include <Python.h>
#include <stdio.h>
#include <numpy/arrayobject.h>
#include <snf3x3.h>

#if (PY_MAJOR_VERSION < 3) && (PY_MINOR_VERSION < 6)
#define PYUNICODE_FROMSTRING PyString_FromString
#else
#define PYUNICODE_FROMSTRING PyUnicode_FromString
#endif

static PyObject * py_snf3x3(PyObject *self, PyObject *args);

struct module_state {
  PyObject *error;
};

#if PY_MAJOR_VERSION >= 3
#define GETSTATE(m) ((struct module_state*)PyModule_GetState(m))
#else
#define GETSTATE(m) (&_state)
static struct module_state _state;
#endif

static PyObject *
error_out(PyObject *m) {
  struct module_state *st = GETSTATE(m);
  PyErr_SetString(st->error, "something bad happened");
  return NULL;
}

static PyMethodDef _snf3x3_methods[] = {
  {"error_out", (PyCFunction)error_out, METH_NOARGS, NULL},
  {"snf3x3", py_snf3x3, METH_VARARGS, "SNF3x3"},
  {NULL, NULL, 0, NULL}
};

#if PY_MAJOR_VERSION >= 3

static int _snf3x3_traverse(PyObject *m, visitproc visit, void *arg) {
  Py_VISIT(GETSTATE(m)->error);
  return 0;
}

static int _snf3x3_clear(PyObject *m) {
  Py_CLEAR(GETSTATE(m)->error);
  return 0;
}

static struct PyModuleDef moduledef = {
  PyModuleDef_HEAD_INIT,
  "_snf3x3",
  NULL,
  sizeof(struct module_state),
  _snf3x3_methods,
  NULL,
  _snf3x3_traverse,
  _snf3x3_clear,
  NULL
};

#define INITERROR return NULL

PyObject *
PyInit__snf3x3(void)

#else
#define INITERROR return

  void
  init_snf3x3(void)
#endif
{
#if PY_MAJOR_VERSION >= 3
  PyObject *module = PyModule_Create(&moduledef);
#else
  PyObject *module = Py_InitModule("_snf3x3", _snf3x3_methods);
#endif

  if (module == NULL)
    INITERROR;
  struct module_state *st = GETSTATE(module);

  st->error = PyErr_NewException("_snf3x3.Error", NULL, NULL);
  if (st->error == NULL) {
    Py_DECREF(module);
    INITERROR;
  }

#if PY_MAJOR_VERSION >= 3
  return module;
#endif
}

static PyObject * py_snf3x3(PyObject *self, PyObject *args)
{
  PyArrayObject* py_A;
  PyArrayObject* py_P;
  PyArrayObject* py_Q;

  long (*A)[3];
  long (*P)[3];
  long (*Q)[3];

  A = NULL;
  P = NULL;
  Q = NULL;

  if (!PyArg_ParseTuple(args, "OOO", &py_A, &py_P, &py_Q)) {
    return NULL;
  }

  A = (long(*)[3])PyArray_DATA(py_A);
  P = (long(*)[3])PyArray_DATA(py_P);
  Q = (long(*)[3])PyArray_DATA(py_Q);

  snf3x3(A, P, Q);

  Py_RETURN_NONE;
}
