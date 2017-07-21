# VideoPopup Build Instruction
This is forked from [VideoPopup][0]

[0]: https://github.com/cvfish/VideoPopup "VideoPopup" 

It is tested on Ubuntu 16.04 system with python2.7.12. Following is the detailed implementation instructions. 

# Small change to the origin repo

# Build the system 

## Requirements 

### Environment 
Ubuntu16.04, Python2.7.12(default)

### Libraries 
**Tips**: I do not use Anaconda. But you can use it certainly. The only thing you should care about is setting right python library path for every single dependency you use. 

*Other libs*: 
These may be installed first. 
1. matlab
2. cmake (>=3.0.0 is better) 
3. Eigen3 (sudo apt-get install libeigen3-dev)
4. boost (sudo apt-get install libboost-dev)
5. cPickle (sudo apt-get install python-pickleshare)
6. matplotlib (pip2 install matplotlib)
7. skimage (pip2 install skimage)

*numpy*: 1.11.0
```shell
sudo apt-get install python-numpy
```

*ceres-solver*:1.10.0
```shell
git clone https://github.com/ceres-solver/ceres-solver
cd ceres-solver-1.10.0
mkdir build 
cd build 
cmake ..
make 
sudo make install 
```
Before cmake it, turn on `BUILD_SHARED_LIBS` switch in `CMakeLists.txt`: 
```Makefile
OPTION(BUILD_SHARED_LIBS "Build Ceres as a shared library." ON)
```

*google.protobuf*: >=3.0.0a3
If you install protobuf as belows, you will get old version of protobuf. 
```shell
sudo apt-get install protobuf-compiler # for protoc 
sudo apt-get install libprotobuf-dev # for C++
sudo apt-get install python-protobuf # for python
```
So, I install new protobuf for python with
```shell
sudo pip2 install 'protobuf>=3.0.0a3'
```
Attention, it will install new protobuf only for python. If you want to use protobuf for C++, you need to install it respectively. 

*cvxpy*: 
If you want to try depth reconstruction, install it. But if you don't use `Anaconda`, do not follow it's website's guide, just install it as follows. Before installing `cvxpy`, you may need to install some necessary libraries, for example, `scipy`. You'd better make a decision according to your only system's response.
```shell
sudo pip2 install cvxpy
```

*vispy*: >=0.5.0
```shell
git clone https://github.com/vispy/vispy
cd vispy 
sudo python setup.py install 
``` 

*PyQt4*: 
```shell
sudo apt-get install python-qt4
sudo apt-get install python-qt4-gl
```
If you don't install `python-qt4-gl`, when you utitlize `vispy`, some errors concerning backend would appear. Their core error is that `cannot import name QtOpenGL`. 

*opengv*:
```shell
git clone https://github.com/laurentkneip/opengv
```
Before compile it, make some small change to `opengv/python/CMakeLists.txt`:line35: 
```Makefile
python -c "import distutils.sysconfig; print 'dist-packages' if distutils.sysconfig.get_python_lib().endswith('dist-packages') else 'site-packages'"
```
change to 
```Makefile
python -c "import distutils.sysconfig; print ('dist-packages' if distutils.sysconfig.get_pyth on_lib().endswith('dist-packages') else 'site-packages')"
```
See, I just add parenthesis to `print` function. Or it will call an error by `cmake`. 
Then, you can compile and install it as following: 
```shell
cd opengv
mkdir build 
cd build 
cmake .. -DBUILD_TESTS=OFF -DBUILD_PYTHON=ON
sudo make install 
```
By switch `BUILD\_SHARED\_LIBS` in `CMakeLists.txt`, you can control shared libs or static libs it generates. If everything works well, it may produce `pyopengv.so` under `/usr/local/lib/python2.7/site-packages`. If not, you may try to copy `pyopengv.so` to this place. 

*OpenSfM dependencies*:
Including `OpenCV`, `Ceres`, `OpenGV`, `Boost`, `Numpy`, `Scipy`, `Networkx`, etc.
See `VideoPopup/libs/mapillary/OpenSfM/README.md` for details. 

## Build

### Small changes to origin `VideoPopup`
When I build it, I come up with some bugs, which may blame on different version of python. So, I make some changes to original code, in order to adapt to current python grammar. 
1. `IndexError` related to numpy boolean array
When you use `A[B]` where `A` is numpy.array object while `B` is a numpy boolean array, you should assure that `A` and `B` strictly have same size. Attention, strictly. 
2. `ValueError` related to numpy boolean array
Look the following code: 
```Python 
if R==None :
```
`R` is `numpy.array` like object, though it may possibly be `None`. In numpy, a boolean array can't be used as bool value, because it may cause ambiguity. So, use a trick to bypass it: 
```Python
if np.array(R==None).any():
```

### Build VideoPopup 
You may use 
```shell
./build.sh
```
to build all libs. You can also build libs respectively. 

## Possible errors when install libraries or build VideoPopup
1. Can not find `Eigen3`. You may need to assign Eigen3 path manually. e.g. Add `-I/usr/include/eigen3` to every `Makefile` under every subdirectory of `VideoPopup/libs`. 

## Possible warning 
1. warning 490
When compiling `OpenSfM`, `warning490` may occur: 
```shell
warning 490: fragment numpy_backward_compatibility not found. 
```
This is not fixed yet. 
2. g++-5 not support mex
This is not fixed as well. You may use g++-4.7. I did not bother to use it. 

## Why Python2
Original codes uses `cPickle` which only exists for `python2`. And some functions like `PyFile_check` used is also exist in `python2` only. 

