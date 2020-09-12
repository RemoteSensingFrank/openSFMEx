'''
Descripttion: 
version: 1.0版本
Author: Frank.Wu
Date: 2020-09-12 13:57:54
LastEditors: Frank.Wu
LastEditTime: 2020-09-12 20:28:24
'''
from flask import Blueprint

monitor = Blueprint('views', __name__,static_folder='static',template_folder='templates')

from . import sys_info
