#
# Unix/Linux Makefile for MATLAB interface to ceres-solver
#

#CXXFLAGS="-std=c++0x -fPIC -O3 -v"
# CXXFLAGS="-std=c++0x -fPIC -O3"
CXXFLAGS="-std=c++0x -fPIC -O3"

# MEX=mex -v GCC='/usr/bin/g++-4.7' CXXFLAGS=$(CXXFLAGS)
MEX=mex CXXFLAGS=$(CXXFLAGS)

$(info $$CXXFLAGS is [${CXXFLAGS}])

INTFACESOBJ=cs_ba.mex mot_reg_cs.mex cs_ba_python

EIGEN_INCLUDE=-I/usr/include/eigen3

CERES_LIBS=-lceres -lcholmod -lccolamd -lcolamd -lamd -lcamd -lcxsparse \
	  -lsuitesparseconfig -lgomp -lglog -lpthread

all: $(INTFACESOBJ)

# $(INTFACESOBJ): $(INTFACESRCS)
# 	$(MEX) $(MEXCFLAGS) $(INTFACESRCS) $(LIB_PATH) $(CERES_LIBS)

$(info $$LIB_PATH is [${LIB_PATH}])
cs_ba.mex: cs_ba.cpp
	$(MEX) cs_ba.cpp $(EIGEN_INCLUDE) $(CERES_LIBS)

mot_reg_cs.mex: mot_reg_cs.cpp

	$(MEX) mot_reg_cs.cpp $(EIGEN_INCLUDE) $(CERES_LIBS)

cs_ba_python:

	swig -python cs_ba_python.i

	g++ -O3 -shared -fPIC cs_ba_python_wrap.c -w -o _cs_ba_python.so \
	    -lceres -lcholmod -lccolamd -lcolamd -lamd -lcamd -lcxsparse \
	    -lsuitesparseconfig -lgomp -lglog -lpthread \
	    -I/usr/lib/python2.7/dist-packages/numpy/core/include \
	    -I/usr/include/python2.7/ \
	    -I/usr/local/include \
	    $(EIGEN_INCLUDE) -L/usr/local/lib
