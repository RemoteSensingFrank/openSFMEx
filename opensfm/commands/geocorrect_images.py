'''
@Descripttion: 
@version: 1.0版本
@Author: Frank.Wu
@Date: 2020-03-16 16:49:40
@LastEditors: Frank.Wu
@LastEditTime: 2020-03-19 14:24:19
'''
import copy
import logging
import time

from opensfm import dataset
from opensfm import geocorrect

logger = logging.getLogger(__name__)

class Command:
    name = 'geocorrect_images'
    help = "Link matches pair-wise matches into tracks"

    def add_arguments(self, parser):
        parser.add_argument('dataset', help='dataset to process')
        parser.add_argument(
            '--reconstruction-index',
            help='index of the reconstruction component to undistort',
            type=int,
            default=0,
        )
        
    def run(self, args):
        data = dataset.DataSet(args.dataset)
        imageNode = data.load_tracks_geocorrect()
        reconstructions = data.load_reconstruction()
        reconstruction=reconstructions[args.reconstruction_index]
        geocorrect.geo_correct_proc(reconstruction,imageNode,data.images(),data)
            