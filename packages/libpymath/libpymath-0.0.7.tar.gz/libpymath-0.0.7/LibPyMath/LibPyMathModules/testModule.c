#define PY_SSIZE_T_CLEAN

#include <Python.h>

static PyObject *testSystem(PyObject *self, PyObject *args) {
    const char *command;
    int sts;

    if (!PyArg_ParseTuple(args, "s", &command))
        return NULL;
    sts = system(command);
    return PyLong_FromLong(sts);
}

static PyObject *testFunction(PyObject *self, PyObject *args, PyObject *kwargs) {
    static char *arguments[] = {
            "first",
            "middle",
            "last",
            "age",
            "numb",
            NULL
    };

    const char *first = "";
    const char *middle = "";
    const char *last = "";
    const unsigned int age = 0;
    const double numb = 0.;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "s|ssid", arguments, &first, &middle, &last, &age, &numb))
        return NULL;

    printf("Your name is %s %s %s and you are %i years old. Your favorite number is %f\n", first, middle, last, age, numb);

    Py_RETURN_NONE;
}

static PyMethodDef SpamMethods[] = {
        {"system", testSystem, METH_VARARGS,
                "Execute a shell command."},
        {"test", (PyCFunction) testFunction, METH_VARARGS | METH_KEYWORDS, "Runs a test function"},
        {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef testModule = {
        PyModuleDef_HEAD_INIT,
        "testModule",   /* name of module */
        NULL, /* module documentation, may be NULL */
        -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
        SpamMethods
};

PyMODINIT_FUNC
PyInit_testModule(void) {
    return PyModule_Create(&testModule);
}
