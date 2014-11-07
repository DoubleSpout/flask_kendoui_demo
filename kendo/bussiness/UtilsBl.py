# -*- coding: utf-8 -*-
#coding=utf-8
from functools import wraps
import flask
from flask import render_template, request, redirect, url_for, sessions, Response, session
import urllib
import types
from sqlalchemy import Text, desc
from datetime import datetime

from kendo.models.dbModel import *

#define utils Class
class Utils(object):


     @staticmethod
     def genResponse(ok, obj):
         if ok:
             status = 1
         else:
             status = 0

         return {
            'status':status,
            'data':obj
         }

     #check sign is Correct
     @staticmethod
     def checkSign(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            #sign logic
            print('in check sign func')
            return f(*args, **kwargs)
        return decorated_function

     #check user token
     @staticmethod
     def checkToken(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            #sign logic
            print('in check token func')
            return f(*args, **kwargs)
        return decorated_function


class DumpToDict(object):
    def __init__(self):
        pass
    def dumpToList(self, result=None):
        if not result:
            result = getattr(self, 'sqlData', None)
        #如果没有sqlData
        if not getattr(self, 'sqlData', None):
            result = self

        #获取model的所遇key
        keyList = self.__mapper__.c.keys()
        #定义数组

        if isinstance(result, list):
            resultLength = len(result)
            tempList = range(resultLength)
            i = 0

            for sqlObj in result:
                tempList[i] = {}
                for key in keyList:
                    tempList[i][key] = getattr(sqlObj, key)
                    #如果是None,则为空
                    if tempList[i][key] is None:
                        tempList[i][key] = ''
                    elif isinstance(tempList[i][key], datetime):
                        tempList[i][key] = tempList[i][key].strftime("%Y-%m-%d %H:%M:%S")
                i += 1
        else:
            tempList = {}
            for key in keyList:
                    tempList[key] = getattr(result, key)
                    #如果是None,则为空
                    if tempList[key] is None:
                        tempList[key] = ''
                    elif isinstance(tempList[key], datetime):
                        tempList[key] = tempList[key].strftime("%Y-%m-%d %H:%M:%S")

        return tempList


#解析kendoui参数的类
class kendouiData(object):

    def parseKendoData(self, paramObj=None):
        if not paramObj:
            paramObj = self.kendoParam

        self.ormSkip = paramObj.get('skip', 0)
        self.ormLimit = paramObj.get('pageSize', 20)
        self.orderBy = paramObj.get('orderBy', 'Id ')
        self.ormFilterList = []
        self.ormFilterValue = []
        self.ormFilterStr = ''

        filter = paramObj.get('filter', {})
        filterList = filter.get('filters', [])

        #循环条件
        count = 0
        for item in filterList:
            if not item:
                continue
            count += 1
            #获得操作变量
            operator = item.get('operator', None)
            #获得字段名
            key = item.get('field', None)

            #如果是等于操作符
            if operator == 'eq':
                self.ormFilterList.append('{0} = :v{1}'.format(key, count))
                self.ormFilterValue.append(item.get('value', None))

            #如果是不等于操作
            elif operator == 'neq':
                self.ormFilterList.append('{0} <> :v{1}'.format(key, count))
                self.ormFilterValue.append(item.get('value', None))

            #如果是起始于操作
            elif operator == 'startswith':
                self.ormFilterList.append('{0} like :v{1}%'.format(key, count))
                self.ormFilterValue.append(item.get('value', None))

            #如果是包含操作
            elif operator == 'contains':
                self.ormFilterList.append('{0} like :%v{1}%'.format(key, count))
                self.ormFilterValue.append(item.get('value', None))

            #如果是结束于操作
            elif operator == 'endswith':
                self.ormFilterList.append('{0} like :%v{1}'.format(key, count))
                self.ormFilterValue.append(item.get('value', None))

            #如果是不包含操作
            elif operator == 'doesnotcontain':
                self.ormFilterList.append('{0} not like :%v{1}%'.format(key, count))
                self.ormFilterValue.append(item.get('value', None))

            #如果是大于等于操作
            elif operator == 'gte':
                self.ormFilterList.append('{0} not >= :%v{1}%'.format(key, count))
                self.ormFilterValue.append(item.get('value', None))

            #如果是大于操作
            elif operator == 'gt':
                self.ormFilterList.append('{0} not > :%v{1}%'.format(key, count))
                self.ormFilterValue.append(item.get('value', None))

            #如果是小于等于操作
            elif operator == 'lte':
                self.ormFilterList.append('{0} not < :%v{1}%'.format(key, count))
                self.ormFilterValue.append(item.get('value', None))

            #如果是小于操作
            elif operator == 'lt':
                self.ormFilterList.append('{0} not <= :%v{1}%'.format(key, count))
                self.ormFilterValue.append(item.get('value', None))

        if filter.get('logic', '') == 'and' and len(self.ormFilterList) > 0:
            self.ormFilterStr = 'and'.join(self.ormFilterList)
        elif filter.get('logic', '') == 'or' and len(self.ormFilterList) > 0:
            self.ormFilterStr = 'or'.join(self.ormFilterList)

        return True

    def getData(self):
        #将kendoui的参数解析为orm的参数
        self.parseKendoData()
        #实例化admin类
        objIns = self.modelClass()
        #查询数据
        adminQuery = self.modelClass.query
        #如果有filter条件
        if self.ormFilterStr != '':
            adminQuery = adminQuery.filter(Text(self.ormFilterStr))\
                                   .params(*self.ormFilterValue)

        adminList = adminQuery\
            .order_by(desc(self.modelClass.Id))\
            .offset(self.ormSkip)\
            .limit(self.ormLimit)\
            .all()

        #将查询的数据转为dict
        objIns.sqlData = adminList
        #查询总数
        total = self.modelClass.query.count()
        return True, {
            'Total': total,
            'AggregateResults':None,
            'Errors':None,
            'Data': objIns.dumpToList()
        }


    #获取并保存数据
    def saveData(self):
        if isinstance(self.saveModel, dict):
            self.saveModel = self.saveModel['models'].get('0', None)

        if not self.saveModel:
            return False, u'更新对象参数有误'

        keyList = self.modelClass.__mapper__.c.keys()

        #将key和字段对应起来
        insObj = {}
        for key in keyList:
            if self.saveModel.get(key, None):
                value = self.saveModel.get(key, None)
                if value is None:
                    continue
                elif value == 'true':
                    value = True
                elif value == 'false':
                    value = False

                insObj[key] = value


        #进行数据库操作
        if insObj['Id'] is None or int(insObj['Id']) == 0:
            #实例化model类
            modelIns = self.modelClass(insObj)
            db.session.add(modelIns)
        else:
            #查询记录
            result = self.modelClass.query.filter(self.modelClass.Id==insObj['Id']).first()
            #更新记录
            for key in insObj:
                setattr(result, key, insObj[key])

        db.session.commit()

        return True, insObj

    def delData(self):
        if type(self.delModel) == dict:
            self.delModel = self.delModel['models'].get('0', None)

        if not self.delModel:
            return False, u'删除对象参数有误'

        delId = self.delModel.get('Id', None)
        if not delId:
            return False, u'Id参数有误'

        #实例化model类
        #insObj = self.modelClass({'Id':int(delId)})
        #进行数据库操作
        self.modelClass.query.filter(self.modelClass.Id == delId).delete()
        #db.session.delete(insObj)
        db.session.commit()

        return True, {}


