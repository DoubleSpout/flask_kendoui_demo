# -*- coding: utf-8 -*-
from functools import wraps
import flask
import hashlib
import time
import httplib
import urllib
import hashlib
import json
import calendar
from datetime import datetime
from flask import render_template, request, redirect, url_for, sessions, Response, session, g
from sqlalchemy import Text, desc
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import load_only, joinedload, dynamic_loader, lazyload, defer, undefer
from sqlalchemy.ext.serializer import loads, dumps


from kendo import app
from kendo.models.adminModel import *
from kendo.models.roleModel import *
from kendo.models.authModel import *
from kendo.bussiness.UtilsBl import kendouiData, SimpleBl
from kendo.bussiness.LoggerBl import log
from kendo.models.dbModel import db
from kendo.bussiness.loginBl import adminBl



class authBl(SimpleBl):

    def __init__(self):
        pass

    # #获取列表页
    # def getList(self):
    #     return self.getData()
    #
    # #添加或者更新一条记录
    # def saveOne(self):
    #
    #     return self.saveData()
    #
    # #删除一条记录
    # def delOne(self):
    #     return self.delData()









