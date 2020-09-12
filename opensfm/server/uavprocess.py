'''
Descripttion: 
version: 1.0版本
Author: Frank.Wu
Date: 2020-09-12 21:49:49
LastEditors: Frank.Wu
LastEditTime: 2020-09-12 22:29:50
'''
import logging
from timeit import default_timer as timer
import copy
import logging
import time


from networkx.algorithms import bipartite

from opensfm import exif
from opensfm import dataset
from opensfm import io
from opensfm import tracking

logger = logging.getLogger(__name__)

class ExtractMetaDataProc:
    def extract(self, dataset):
        start = time.time()
        data = dataset.DataSet(dataset)

        exif_overrides = {}
        if data.exif_overrides_exists():
            exif_overrides = data.load_exif_overrides()

        camera_models = {}
        for image in data.images():
            if data.exif_exists(image):
                logging.info('Loading existing EXIF for {}'.format(image))
                d = data.load_exif(image)
            else:
                logging.info('Extracting EXIF for {}'.format(image))
                d = self._extract_exif(image, data)

                if image in exif_overrides:
                    d.update(exif_overrides[image])

                data.save_exif(image, d)

            if d['camera'] not in camera_models:
                print(d)
                camera = exif.camera_from_exif_metadata(d, data)
                camera_models[d['camera']] = camera

        # Override any camera specified in the camera models overrides file.
        if data.camera_models_overrides_exists():
            overrides = data.load_camera_models_overrides()
            if "all" in overrides:
                for key in camera_models:
                    camera_models[key] = copy.copy(overrides["all"])
                    camera_models[key].id = key
            else:
                for key, value in overrides.items():
                    camera_models[key] = value
        data.save_camera_models(camera_models)

        end = time.time()
        with open(data.profile_log(), 'a') as fout:
            fout.write('extract_metadata: {0}\n'.format(end - start))

    '''
    name: 解析exif文件
    msg: 
    param {type} 
    return {type} 
    '''
    def _extract_exif(self, image, data):
         # EXIF data in Image
        d = exif.extract_exif_from_file(data.open_image_file(image))

        # Image Height and Image Width
        if d['width'] <= 0 or not data.config['use_exif_size']:
            d['height'], d['width'] = data.image_size(image)

        d['camera'] = exif.camera_id(d)

        return d

    '''
    name: 判断文件是否为本地文件或为ftp文件，如果为ftp文件则下载，否则直接解析
    msg: 
    param {type} 
    return {type} 
    '''
    def _check_local(self,datapath):
        pass