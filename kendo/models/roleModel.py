# -*- coding: utf-8 -*-
from datetime import datetime
from flask import Flask

from flask.ext.sqlalchemy import SQLAlchemy
from kendo import app
from kendo.models.dbModel import *
from kendo.models.authModel import *
from kendo.bussiness.UtilsBl import DumpToDict
import json

#用户权限表
class role(db.Model, DumpToDict):
    #表名
    __tablename__ = 'role'

    Id = db.Column(db.Integer, primary_key=True)
    roleName = db.Column(db.String(50))
    roleTips = db.Column(db.String(50))
    code1 = db.Column(db.String(50))
    code2 = db.Column(db.String(50))

    updateTime = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now)
    writeTime = db.Column(db.DateTime, default=datetime.now)

    auths = db.relationship('auth', secondary='role_auth',
        backref=db.backref('role', lazy='select'), lazy='select')

    def __init__(self, modelDict={}):
        self.Id = modelDict.get('Id', None)
        self.roleName = modelDict.get('roleName', None)
        self.roleTips = modelDict.get('roleTips', None)


#关联表
class roleAuth(db.Model):
    __tablename__ = 'role_auth'

    Id = db.Column(db.Integer, primary_key=True)
    roleId = db.Column(db.Integer, db.ForeignKey('role.Id'), nullable=False)
    authId = db.Column(db.Integer, db.ForeignKey('auth.Id'), nullable=False)

    db.UniqueConstraint('roleId', 'authId', name='unique_1')

    def __init__(self, modelDict={}):
        self.Id = modelDict.get('Id', None)
        self.roleId = modelDict.get('roleId', None)
        self.authId = modelDict.get('authId', None)