'''
Descripttion: 
version: 1.0版本
Author: Frank.Wu
Date: 2020-09-12 21:41:55
LastEditors: Frank.Wu
LastEditTime: 2020-09-12 22:24:44
'''
import os, sys

from opensfm.server import serverutil

from flask_restful import Resource
from flask import Response,make_response

class HelloWorld(Resource):
    def get(self):
        return "HEllO WORLD"

'''
name: 列出当前服务器本地所有影像文件
msg: 
param None
return 影像文件列表
'''
class ListLocalImageFolders(Resource):
    def get(self):
        dirs=[]
        try:
            dirs=os.listdir(serverutil.local_data_directory)
        except Exception:
            dirs=[]
        data=serverutil.make_standard_response(dirs,"影像文件列表",0)
        return make_response(data, 200)


# 解析源数据接口
# class ExtractMetaDataRoute(Resource):
#     def get(self):
