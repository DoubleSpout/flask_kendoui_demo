# -*- coding: utf-8 -*-
from datetime import datetime
from flask import Flask

from flask.ext.sqlalchemy import SQLAlchemy
from kendo import app
from kendo.models.dbModel import db
from kendo.models.roleModel import *
from kendo.bussiness.UtilsBl import DumpToDict
import json

#管理员表
class admin(db.Model, DumpToDict):
    #表名
    __tablename__ = 'admin'

    Id = db.Column(db.Integer, primary_key=True, index=True)
    admin = db.Column(db.String(50), unique=True, )
    password = db.Column(db.String(50))
    avatar = db.Column(db.String(255))
    tips = db.Column(db.String(50))
    isShow = db.Column(db.Boolean, default=True)
    updateTime = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now)
    writeTime = db.Column(db.DateTime, default=datetime.now)
    code1 = db.Column(db.String(50))
    code2 = db.Column(db.String(50))
    code3 = db.Column(db.String(50))
    code4 = db.Column(db.String(50))

    roles = db.relationship('role', secondary='admin_role',
        backref=db.backref('admin', lazy='select'), lazy='select')

    def __init__(self, modelDict={}):
        self.Id = modelDict.get('Id', None)
        self.admin = modelDict.get('admin', None)
        self.password = modelDict.get('password', None)
        self.tips = modelDict.get('tips', None)
        self.isShow = modelDict.get('isShow', True)
        self.writeTime = modelDict.get('writeTime', datetime.now)
        self.avatar = modelDict.get('avatar', None)


#关联表
class adminRole(db.Model):
    __tablename__ = 'admin_role'

    Id = db.Column(db.Integer, primary_key=True)
    adminId = db.Column(db.Integer, db.ForeignKey('admin.Id'), nullable=False)
    roleId = db.Column(db.Integer, db.ForeignKey('role.Id'), nullable=False)

    db.UniqueConstraint('adminId', 'roleId', name='unique_1')

    def __init__(self, modelDict={}):
        self.Id = modelDict.get('Id', None)
        self.adminId = modelDict.get('adminId', None)
        self.roleId = modelDict.get('roleId', None)

