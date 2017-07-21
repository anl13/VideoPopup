"""
Doing piecewise rigid reconstruction on a sequence.
Assume we have tracks and the labels of these tracks
"""

import os
import numpy as np
import cPickle as pickle
import itertools
import collections

import sys
sys.path.append('../../libs/mapillary/OpenSfM/')
from opensfm import reconstruction
from opensfm import mesh
from opensfm import types

from PyQt4 import QtGui
import sys

from video_popup.visualization import qt_app_persp
from video_popup.utils import util_opensfm as util

# from video_popup.visualization import vispy_util_persp

import scipy.io
import glob as glob

#expr = 'Kitti'
expr = 'two-men'

my_init = False

if(expr == 'two-men'):
    #load segmentation result 
    seg_file = '../../data/Two-men/images/broxmalik_size4/broxmalikResults' \
               '/f1t25/v5_d4/vw10_nn10_k5_thresh10000_max_occ10_op0_cw2.5/init200/mdl2000_pw10_oc10_engine0_it5/results.pkl'

    K = np.array([[1200, 0,  479.5],
                  [0, 1200,  269.5],
                  [0,    0,      1]])

    with open(seg_file, 'r') as f:
        seg = pickle.load(f)

    W = seg['W']
    Z = seg['Z']
    labels = seg['labels_objects']

    labels[labels == 1] = 0
    labels[labels == 4] = 0
    labels[labels == 2] = 1
    labels[labels == 3] = 2

    images = seg['images']

    my_data = (W, Z, labels, K, images)

    my_init = True

seg_path, file_name = os.path.split(seg_file)

input = seg_path + '/OpenSfM/' + 'input.pkl'
print("input.pkl path:")
print(input)

try:
    util.ensure_dir(input)
    with open(input, 'r') as f:
        data, graphs = pickle.load(f)
except:
    data, graphs = util.tracks_to_opensfm_input(my_data)
    with open(input, 'w') as f:
        pickle.dump((data, graphs), f, True)

save_mesh = 0

data.config['seg_path'] = seg_path
# data.config['label'] = 1
# reconstruction.incremental_reconstruction(data, graphs[1])

scene_reconstructions = {}

for label in graphs:

    data.config['label'] = label

    try:
        # with open(seg_path + '/OpenSfM/' + 'reconstruction{:02d}.json'.format(label)) as f:
        reconstructions = data.load_reconstruction()
    except:
        reconstruction.incremental_reconstruction(data, graph=graphs[label], my_init=my_init)
        reconstructions = data.load_reconstruction()

    if(save_mesh):
        for i, r in enumerate(reconstructions):
            for shot in r.shots.values():
                if shot.id in graphs[label]:
                    vertices, faces = mesh.triangle_mesh(shot.id, r, graphs[label], data)
                    shot.mesh = types.ShotMesh()
                    shot.mesh.vertices = vertices
                    shot.mesh.faces = faces
        data.save_reconstruction(reconstructions,
                                 filename='reconstruction.meshed.json')

    scene_reconstructions[label] = reconstructions

    if(len(reconstructions) == 1):
        """there is only one reconstruction for this, probably good"""
        reconstruct = reconstructions[0]
    else:
        print "have trouble with reconstruction of label {:d}".format(label)

# ## merge reconstructions together
# util.MySceneCanvas(scene_reconstructions, data, K)

#show qt app
show = False
appQt = QtGui.QApplication(sys.argv)

# scene_reconstructions[0] = scene_reconstructions[1]
# scene_reconstructions.pop(1,None)
#my_canvas = util.MyCanvas(scene_reconstructions[0][0], data.image_files, has_color=0)

vispy_reconstructions = util.opensfm_output_to_vispy(scene_reconstructions, my_data)
vispy_file = seg_path + '/OpenSfM/' + 'vispy_output.pkl'
try:
    util.ensure_dir(vispy_file)
    with open(vispy_file, 'r') as f:
        vispy_reconstructions = pickle.load(f)
except:
    with open(vispy_file, 'w') as f:
        pickle.dump(vispy_reconstructions, f, True)

image_files = collections.OrderedDict(sorted(data.image_files.items())).values()

win = qt_app_persp.MainWindow(vispy_reconstructions, image_files, K, False)

win.show()
appQt.exec_()
