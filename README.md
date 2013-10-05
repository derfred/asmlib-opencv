asmlib-opencv
=============

This repo is a fork of https://code.google.com/p/asmlib-opencv/ to demonstrate how 3rd party C++ modules can be integrated into the Python bindings for OpenCV. This code depends on https://github.com/Itseez/opencv/pull/1571.

# Build instructions
The following lines are copy-and-pastable instructions to build the OpenCV branch in the Pull Request above and this repository.

## Build OpenCV branch
This will download and build the code from the dependant branch and then install it into a temporary directory.

```bash
git clone https://github.com/derfred/opencv.git opencv_external
cd opencv_external
git checkout external_python_modules
mkdir build
cd build
cmake -D CMAKE_INSTALL_PREFIX=../../opencv_external_install ..
make
make install
```

On my machine (MacOS Mountain Lion with Python installed via homebrew) I had to specify the Python executable. Should you have problems building, try the following changes to the cmake line:
```bash
cmake -D CMAKE_INSTALL_PREFIX=../../opencv_external_install -D PYTHON_EXECUTABLE=/usr/local/bin/python -D PYTHON_INCLUDE_DIR=/usr/local/Cellar/python/2.7.4/Frameworks/Python.framework/Headers -D PYTHON_LIBRARY=/usr/local/Cellar/python/2.7.4/Frameworks/Python.framework/Versions/2.7/lib/libpython2.7.dylib ..
```

## Build ASMLib (this repository)
```bash
git clone https://github.com/derfred/asmlib-opencv.git
cd asmlib-opencv/src
mkdir build
cd build
OpenCV_DIR=../../../opencv_external_install/share/OpenCV/ cmake ..
make
```

# Run the demo
If you have followed the steps above then the following will run the Python demo on your webcam, assuming your CWD is src/demo.
```bash
PYTHONPATH="../build/lib:$PYTHONPATH" python demo.py -f -pc -m ../../data/muct76.model -C ../../data/haarcascade_frontalface_alt.xml
```
