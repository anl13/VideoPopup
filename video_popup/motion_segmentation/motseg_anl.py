""" video popup code

Code for the paper "Video Pop-up: Monocular 3D Reconstruction of
Dynamic Scenes"

"""

import numpy as np
import glob as glob

import video_popup_pb2
import persp_segmentation as ps

segmentaton_para = video_popup_pb2.SegmentationPara()
neighborhood_para = video_popup_pb2.NeighborhoodPara()

expr = 'anliang'

downsampling = 1
saving_seg_result = 0
#from IPython import embed; embed()

if(expr == 'anliang'):

    start_frame = 1
    end_frame = 30

    neighborhood_para.dist_threshold = 10000
    neighborhood_para.top_frames_num = 5
    neighborhood_para.max_occlusion_frames = 10
    neighborhood_para.occlusion_penalty = 0
    neighborhood_para.velocity_weight = 10

    segmentaton_para.images_path = '../../data/anliang/*.jpg'
    images = sorted(glob.glob(segmentaton_para.images_path))[0: end_frame - start_frame + 1]
    segmentaton_para.min_vis_frames = 5

    model_fitting_para = segmentaton_para.model_fitting_para

    segmentaton_para.tracks_path = '../../data/anliang/tracking/broxmalik_Size2/broxmalikResults/broxmalikTracks203.dat'
    model_fitting_para.mdl = 2000
    model_fitting_para.graph_cut_para.pairwise_weight = 10
    model_fitting_para.graph_cut_para.pairwise_sigma = 0.5
    model_fitting_para.graph_cut_para.overlap_cost = 10
    model_fitting_para.graph_cut_para.engine = 0
    model_fitting_para.iters_num = 5

    # segmentaton_para.tracks_path = '../../data/Kitti/05/broxmalik_Size4/broxmalikResults/broxmalikTracks15.dat'
    # model_fitting_para.mdl = 2000
    # model_fitting_para.graph_cut_para.pairwise_weight = 10000
    # model_fitting_para.graph_cut_para.overlap_cost = 10
    # model_fitting_para.graph_cut_para.engine = 0
    # model_fitting_para.iters_num = 5

    # segmentaton_para.tracks_path = '../../data/Kitti/05/broxmalik_Size8/broxmalikResults/broxmalikTracks15.dat'
    # model_fitting_para.mdl = 2000
    # model_fitting_para.graph_cut_para.pairwise_weight = 10000
    # model_fitting_para.graph_cut_para.overlap_cost = 10
    # model_fitting_para.graph_cut_para.engine = 0
    # model_fitting_para.iters_num = 5

    downsampling = 4
    saving_seg_result = 1

print(start_frame)

#from IPython import embed; embed()

ps.persp_segmentation(neighborhood_para, segmentaton_para, model_fitting_para, images, start_frame, end_frame,
                      saving_seg_result = saving_seg_result, downsampling = downsampling)
