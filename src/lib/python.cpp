#include <Python.h>

#define MODULESTR "asmlib"

#include "asmmodel.h"

#include "opencv2/python/cv2.hpp"
#include "opencv2/python/cv2support.cpp"

using namespace cv;
using namespace ASMLib;

typedef std::vector<ASMLib::ASMFitResult> vector_ASMFitResult;

#include "ASMLib_generated_types.h"

template<> struct pyopencvVecConverter<ASMLib::ASMFitResult>
{
    static bool to(PyObject* obj, std::vector<ASMLib::ASMFitResult>& value, const ArgInfo info)
    {
        return pyopencv_to_generic_vec(obj, value, info);
    }

    static PyObject* from(const std::vector<ASMLib::ASMFitResult>& value)
    {
        return pyopencv_from_generic_vec(value);
    }
};

template<> bool pyopencv_to(PyObject* src, ASMLib::ASMModel& dst, const ArgInfo info)
{
    if( src == NULL || src == Py_None )
        return true;
    if(!PyObject_TypeCheck(src, &pyopencv_ASMModel_Type))
    {
        failmsg("Expected ASMModel for argument '%%s'", info.name);
        return false;
    }
    dst = *((pyopencv_ASMModel_t*)src)->v;
    return true;
}

#include "ASMLib_generated_funcs.h"


static PyMethodDef methods[] = {
#include "ASMLib_generated_func_tab.h"
  {NULL, NULL, 0, NULL},
};

extern "C" CV_EXPORTS void initasmlib();

void initasmlib() {
  import_array();

  #include "ASMLib_generated_type_reg.h"

  PyObject* m = Py_InitModule(MODULESTR, methods);
  PyObject* d = PyModule_GetDict(m);

  opencv_error = PyErr_NewException((char*)MODULESTR".error", NULL, NULL);
  PyDict_SetItemString(d, "error", opencv_error);

  #include "ASMLib_generated_const_reg.h"
}
