# -*- coding: utf-8 -*-
import os
import sys
import getopt
import flask
from kendo import app
from kendo import config
from flask.ext.sqlalchemy import SQLAlchemy
from kendo.models.dbModel import db

reload(sys)
sys.setdefaultencoding('utf-8')


#获取配置参数并return {'error':1,'data':'不能补签过期日期'}
__opts, _ = getopt.getopt(sys.argv[1:], "e:") #获取命令行参数
__scritpEnv = ""

for name, value in __opts:
    if name == "-e": #获取命令行参数e
        __scritpEnv = value
if __scritpEnv.lower() == "debug":
    app.config.from_object(config.Debug())
else:
    app.config.from_object(config.Production())

print('running env: {0}'.format(app.config['ENV']))

#session支持
app.secret_key = app.config['SESSION_KEY']

def mkdirFn(path):
    # 引入模块
    
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\") 
 
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
 
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        print path+' create success'
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print path+' is exist'
        return False

#计算路径，然后创建文件夹
curPath = os.path.split(os.path.realpath(__file__))[0]
logsPath = curPath + os.sep + 'logs'
uploadPath = curPath + os.sep + 'kendo' + os.sep + 'static' + os.sep +'upload'

mkdirFn(logsPath)#创建日志路径
mkdirFn(uploadPath)#创建上传路径

from kendo.controllers import *
from kendo.models import *
from kendo.route import *

#db access
db.create_all()

if __name__ == '__main__':
    from kendo.bussiness.loginBl import adminBl
    #初始化管理员及权限
    adminBl.initAdmin()
    app.run(host=app.config.get("HOST"),port=app.config.get("PORT"))

    
    
    
