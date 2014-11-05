# -*- coding: utf-8 -*-
#coding=utf-8
from functools import wraps
import flask
from flask import render_template, request, redirect, url_for, sessions, Response, session
import urllib
import types
import datetime
import kendo.bussiness.loginBl

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


     #检查用户是否登录，并且获取管理员的权限
     @staticmethod
     def authLogin(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            #判断是否登录
            if not session.get('adminId', None):
                return redirect(url_for('loginPage'))

            #获取管理员的信息
            adminIns = loginBl.adminBl()
            adminIns.adminId = session.get('adminId')
            adminObj = adminIns.getAdminById()
            adminAuth = adminIns.getAdminAuth()
            #将admin写入request对象
            request['admin'] = adminObj
            request['auth'] = adminAuth
            #返回参数管理员类和管理员权限类
            return f(*args, **kwargs)

        return decorated_function


class DumpToDict(object):
    def __init__(self):
        pass
    def dumpToList(self, result=None):
        if not result:
            result = self.sqlData

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
                    if isinstance(tempList[i][key], datetime.date):
                        tempList[i][key] = tempList[i][key].strftime("%Y-%m-%d %H:%M:%S")
                i += 1
        else:
            tempList = {}
            for key in keyList:
                    tempList[key] = getattr(result, key)
                    if isinstance(tempList[key], datetime.date):
                        tempList[key] = tempList[key].strftime("%Y-%m-%d %H:%M:%S")

        return tempList