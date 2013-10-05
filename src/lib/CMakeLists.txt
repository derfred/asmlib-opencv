CMAKE_MINIMUM_REQUIRED (VERSION 2.6)
PROJECT( asmlib-opencv )
FIND_PACKAGE( OpenCV REQUIRED )
SET(LIB_SRC_LIST modelfile.cpp asmmodel.cpp shapevec.cpp similaritytrans.cpp afreader.cpp modelimage.cpp  shapemodel.cpp shapeinfo.cpp)

#INCLUDE_DIRECTORIES( ${OPENCV_INCLUDE_DIR} )

ADD_LIBRARY( asm STATIC ${LIB_SRC_LIST} )

# ---------------------------------------------------------
# Python interface
# ---------------------------------------------------------

set(asmlib_opencv_hdrs
    "${CMAKE_CURRENT_SOURCE_DIR}/shapemodel.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/shapevec.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/asmmodel.h")

set(asmlib_cv2_generated_hdrs
    "${CMAKE_CURRENT_BINARY_DIR}/ASMLib_generated_funcs.h"
    "${CMAKE_CURRENT_BINARY_DIR}/ASMLib_generated_func_tab.h"
    "${CMAKE_CURRENT_BINARY_DIR}/ASMLib_generated_types.h"
    "${CMAKE_CURRENT_BINARY_DIR}/ASMLib_generated_type_reg.h"
    "${CMAKE_CURRENT_BINARY_DIR}/ASMLib_generated_const_reg.h")

add_custom_command(
   OUTPUT ${asmlib_cv2_generated_hdrs}
   COMMAND ${PYTHON_EXECUTABLE} "${OpenCV_CONFIG_PATH}/gen2.py" ASMLib ${CMAKE_CURRENT_BINARY_DIR} ${asmlib_opencv_hdrs}
   DEPENDS ${asmlib_opencv_hdrs})

FIND_PACKAGE(PythonInterp)
FIND_PACKAGE(PythonLibs)

INCLUDE_DIRECTORIES(${PYTHON_INCLUDE_PATH})
INCLUDE_DIRECTORIES(${PYTHON_NUMPY_INCLUDE_DIRS})
INCLUDE_DIRECTORIES(${CMAKE_CURRENT_BINARY_DIR})
INCLUDE_DIRECTORIES(${OpenCV_INCLUDE_DIRS})

add_library(asmlib SHARED python.cpp ${asmlib_cv2_generated_hdrs})
target_link_libraries(asmlib ${PYTHON_LIBRARIES})
target_link_libraries(asmlib asm)
target_link_libraries(asmlib ${OpenCV_LIBS})

set_target_properties(asmlib PROPERTIES
                      PREFIX ""
                      OUTPUT_NAME asmlib
                      SUFFIX ".so")
