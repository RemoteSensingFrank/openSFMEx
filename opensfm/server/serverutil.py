'''
Descripttion: 
version: 1.0版本
Author: Frank.Wu
Date: 2020-09-12 22:05:34
LastEditors: Frank.Wu
LastEditTime: 2020-09-12 22:25:39
'''
import json
from flask import Flask, request ,jsonify

'''
name: 文件存储路径，这个路径式相对于运行的server的路径
msg: 
param {type} 
return {type} 
'''
local_data_directory="../data/"


'''
name:数据组织为标准化的输出格式 
msg: 
param 错误代码，无错误返回0，错误信息，数据情况
return {type} 
'''
def make_standard_response(code,info,data):
    standard_data={}
    standard_data['code']=code
    standard_data['info']=info
    standard_data['data']=data  
    return jsonify(standard_data)