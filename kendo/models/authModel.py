# -*- coding: utf-8 -*-
from datetime import datetime
from flask import Flask

from flask.ext.sqlalchemy import SQLAlchemy
from kendo import app
from kendo.models.dbModel import *
from kendo.bussiness.UtilsBl import DumpToDict
import json

#用户权限表
class auth(db.Model, DumpToDict):
    #表名
    __tablename__ = 'auth'

    Id = db.Column(db.Integer, primary_key=True)
    authName = db.Column(db.String(50))
    groupName = db.Column(db.String(50))
    authUrl = db.Column(db.String(50))
    isMenu = db.Column(db.Boolean) #是否为菜单，如果是，则这个url将会在菜单显示出来

    code1 = db.Column(db.String(50))
    code2 = db.Column(db.String(50))

    updateTime = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now)
    writeTime = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, authName=None, groupName=None, authUrl=None, isMenu=False):
        self.authName = authName
        self.groupName = groupName
        self.authUrl = authUrl
