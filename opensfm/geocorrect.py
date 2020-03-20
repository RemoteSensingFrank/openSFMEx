'''
@Descripttion: 
@version: 1.0版本
@Author: Frank.Wu
@Date: 2020-03-16 16:46:02
@LastEditors: Frank.Wu
@LastEditTime: 2020-03-20 17:40:40
'''
import logging
import sys
import os

from osgeo import gdal
from osgeo import osr
from opensfm import tracking
from pyproj import Proj

logger = logging.getLogger(__name__)

'''
    经纬度转换为UTM投影坐标
    @param lng:输入经度
    @param lat:输入纬度
    return x,y 投影坐标
'''
def lla2utm(lng,lat):
    nZone = lng/6+31
    pj = Proj(proj='utm',zone=nZone,ellps='WGS84', preserve_units=False)
    return pj(lng,lat)

'''
    通过空三结果和连接点对影像进行几何校正的过程
    @param reconstruction：空三后的结果
    @param imageNodes：影像点
    @param imageList：影像集
    @param dataset：数据集
'''
def geo_correct_proc(reconstruction,imageNodes,imageList,dataset):
    dir = dataset.create_geo_correct_dir()
    for item in imageList:
        (filename, extension) = os.path.splitext(item)
        gcp_list = geo_correct_GCPs(reconstruction,imageNodes[item],item)
        # f = open(filename+"out.txt", "w") 
        # for itemgcp in gcp_list:
        #     print(itemgcp.GCPX,itemgcp.GCPY,itemgcp.GCPX,itemgcp.GCPPixel,itemgcp.GCPLine ,file=f)
        # f.close()
        imgpath = dataset.data_path+'images/'+item
        outpath = dir+'/'+filename+'.tif'
        gdal_geo_correction(imgpath,gcp_list,outpath,0.5)

'''
    计算影像上的点的地理坐标
    @param reconstruction：空三后的结果
    @param node:影像连接点
    @param image:影像
    @return 返回GCP点
'''
def geo_correct_GCPs(reconstruction,node,image):
    points = reconstruction.points
    shots  = reconstruction.shots
    reference_lla = reconstruction.reference_lla
    shot = shots[image]
    size = [shot.camera.width,shot.camera.height]
    gcps_list =[]
    refGeo=(lla2utm(reference_lla['longitude'], reference_lla['latitude']))

    listUnique=[]
    for item1 in node:
        find = False
        for item2 in listUnique:
            if(abs(float(item1[2])-float(item2[2]))<0.0001 and abs(float(item2[3])-float(item2[3]))<0.0001):
                find=True
        if(find):
            continue
        else:
            listUnique.append(item1)

    width = float(size[0])
    height = float(size[1])

    maxsize = max(float(size[0]), float(size[1]))

    for item in listUnique:
        # 这个判断很没有道理，
        # 主要是对数据结构不是很清楚，所以只能尝试
        if (item[0] in points):
            gcp=[]
            gcp.append(points[item[0]].coordinates[0]+refGeo[0])
            gcp.append(points[item[0]].coordinates[1]+refGeo[1])
            gcp.append(points[item[0]].coordinates[2])
            gcp.append(float(item[2])* maxsize - 0.5 + width / 2.0)
            gcp.append(float(item[3])* maxsize - 0.5 + height / 2.0)
            gcps_list.append(gdal.GCP(gcp[0],gcp[1],gcp[2],gcp[3],gcp[4]))
    return gcps_list

'''
    针对单个影像进行几何校正
    @param image:待校正影像
    @param gcps:控制点
    @param output:输出校正结果
    @param resolution:分辨率
'''
def gdal_geo_correction(image,gcps,output,resolution):
    print(image)
    datasetIn=gdal.Open(image)
    sr = osr.SpatialReference()
    sr.SetWellKnownGeogCS('WGS84')
    datasetIn.SetGCPs(gcps, sr.ExportToWkt())

    dst_ds = gdal.Warp(output, datasetIn, format='GTiff', tps=True,
                       xRes=resolution, yRes=resolution, dstNodata=-3000, srcNodata=-3000,
                       resampleAlg=gdal.GRIORA_Bilinear, outputType=gdal.GDT_Float32)
    # print dst_ds
    del datasetIn, sr
    return 0
            
    


