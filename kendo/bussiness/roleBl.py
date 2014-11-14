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
from kendo.utils.pyquerystring.querystring import parse

from kendo import app
from kendo.models.adminModel import *
from kendo.models.roleModel import *
from kendo.models.authModel import *
from kendo.bussiness.UtilsBl import kendouiData, SimpleBl
from kendo.bussiness.LoggerBl import log
from kendo.models.dbModel import db
from kendo.bussiness.loginBl import adminBl



class roleBl(SimpleBl):

    def __init__(self):
        pass

    # #获取列表页
    def getList(self):
        ok, dict = self.getData()

        if not ok:
            return ok, dict
        #如果为空
        if len(self.sqlData) == 0:
            return ok, dict
        resultList = []

        for item in self.sqlData:
            resultDict = {}
            resultDict['Id'] = item.Id
            resultDict['roleName'] = item.roleName
            resultDict['roleTips'] = item.roleTips
            resultDict['code1'] = item.code1
            resultDict['code2'] = item.code2
            resultDict['updateTime'] = item.updateTime.strftime("%Y-%m-%d %H:%M:%S")
            resultDict['writeTime'] = item.writeTime.strftime("%Y-%m-%d %H:%M:%S")
            resultDict['auths'] = []
            #获取角色的权限列表
            if isinstance(item.auths, list) and len(item.auths) > 0:
                for authIns in item.auths:
                    resultDict['auths'].append({
                        'Id':authIns.Id,
                        'authName':authIns.authName,
                        'groupName':authIns.groupName,
                        'authUrl':authIns.authUrl,
                        'isMenu':authIns.isMenu,
                        'code1':authIns.code1,
                        'code2':authIns.code2,
                        'updateTime':authIns.updateTime.strftime("%Y-%m-%d %H:%M:%S"),
                        'writeTime':authIns.writeTime.strftime("%Y-%m-%d %H:%M:%S")
                    })

            resultList.append(resultDict)

        return ok, {
            'Total': dict['Total'],
            'AggregateResults':None,
            'Errors':None,
            'Data': resultList
        }

    #     return
    #
    #添加或者更新一条记录
    def saveOne(self):

        self.saveModel = parse(self.saveModel)

        if isinstance(self.saveModel, dict):
            self.saveModel = self.saveModel['models'].get('0', None)

        if not self.saveModel:
            return False, u'更新对象参数有误'
        try:
            self.saveModel['auths'] = json.loads(self.saveModel.get('auths', '[]'))
        except Exception as err:
            return False, err

        #进行数据库操作
        if self.saveModel['Id'] is None or int(self.saveModel['Id']) == 0:
            #实例化model类
            modelIns = self.modelClass(self.saveModel)
            db.session.add(modelIns)
            db.session.commit()
            for authObj in self.saveModel['auths']:
                tempIns = roleAuth({
                    'roleId':modelIns.Id,
                    'authId':authObj['Id']
                })
                db.session.add(tempIns)
        else:
            #查询记录
            result = self.modelClass.query.filter(self.modelClass.Id==self.saveModel['Id']).first()
            #更新记录
            for key in self.saveModel:
                setattr(result, key, self.saveModel[key])

        db.session.commit()

        return True,{}
    #
    # #删除一条记录
    def delOne(self):
         return self.delData()









