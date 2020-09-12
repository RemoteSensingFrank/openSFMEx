'''
Descripttion: 
version: 1.0版本
Author: Frank.Wu
Date: 2020-09-12 11:36:58
LastEditors: Frank.Wu
LastEditTime: 2020-09-12 22:16:36
'''

from os.path import abspath, join, dirname
import sys
sys.path.insert(0, abspath(join(dirname(__file__), "..")))

import argparse
import logging


from opensfm import server
from opensfm.server import views
from opensfm.server import uavporcessRoute
from opensfm.server.views.custom_filters import format_time, format_size, socket_type, socket_family, format_addr_port

# from server import server_monitor
# from opensfm import commands
from opensfm import log
log.setup()

from flask import Flask
from flask_restful import Api
from flask_restful import Resource

app = Flask(__name__)
app.add_template_filter(format_time)
app.add_template_filter(format_size)
app.add_template_filter(socket_type)
app.add_template_filter(socket_family)
app.add_template_filter(format_addr_port)
app.register_blueprint(server.views.monitor,url_prefix="/monitor")

api = Api(app)


api.add_resource(uavporcessRoute.HelloWorld, '/test')
api.add_resource(uavporcessRoute.ListLocalImageFolders, '/listfiles')


# 实例化，可视为固定格式
# app = Flask(__name__)
# class Test(Resource):
#     # 如果add_resource绑定了多个url，如果没有传参，可以将视图函数中的参数设置为None
#     # 此时即使url中没有传递参数，也不会报错
#     def post(self):
#         return "check"
 
        
# server monitor pages
# api.add_resource(Test, '/test')
# api.add_resource(server.server_monitor.Monitor.cpu, '/cpu/')
# api.add_resource(server.server_monitor.Monitor.ram, '/ram/')
# api.add_resource(server.server_monitor.Monitor.disk, '/disk/')
# api.add_resource(server.server_monitor.Monitor.process, '/process/')

if __name__ == '__main__':
    # app.run(host, port, debug, options)
    # 默认值：host="127.0.0.1", port=5000, debug=False
    app.run(host="0.0.0.0", port=5000)