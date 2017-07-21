all:
	swig -python tracks.i

# Because it uses PyFile_check(..) functions that only exist in python2, so
# We have to compile it using python2, except that we change its code.

	g++ -g -shared -fPIC tracks_io.cpp tracks_wrap.c -w -o _tracks.so \
	  -I/usr/local/lib/python2.7/dist-packages/numpy/core/include \
	  -I/usr/include/python2.7/

#	g++ -g -shared -fPIC tracks_io.cpp tracks_wrap.c -w -o _tracks.so \
	  -I/home/al17/anaconda3/lib/python3.6/site-packages/numpy/core/include \
	  -I/home/al17/anaconda3/include/python3.6m/
