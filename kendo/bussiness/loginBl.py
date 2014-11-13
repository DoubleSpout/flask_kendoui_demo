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
from kendo.bussiness.UtilsBl import kendouiData
from kendo.bussiness.LoggerBl import log
from kendo.models.dbModel import db




class adminBl(kendouiData):

    def __init__(self, username=None, password=None, tips=None):
        self.username = username
        self.password = password
        self.tips = tips
        pass

    #检查是否登录成功
    def checkLogin(self):
        #实例化admin类
        adminIns = admin()

        postUserName = self.username
        postPassword = self.password
        userObj = admin.query.filter_by(admin=postUserName, isShow=True).first()
        if not userObj:
            return False, u'未找到此管理员'
        postPassword = hashlib.md5(postPassword+app.config['ADMIN_PASSWORD_SALT']).hexdigest().upper()
        if postPassword != userObj.password:
            return False, u'用户名密码错误'

        adminIns.sqlData = userObj
        return True, adminIns.dumpToList()

    #获取管理员信息方法
    def getAdminById(self):
        adminIns = admin()

        userObj = admin.query.filter_by(Id=self.adminId, isShow=True).first()
        if not userObj:
            return False, u'未找到此管理员'

        adminIns.sqlData = userObj
        return True, adminIns.dumpToList()

    #获取管理员的权限方法
    def getAdminAuth(self):
        userObj = admin.query.filter_by(Id=self.adminId, isShow=True).first()
        if not userObj:
            return False, u'未找到此管理员'

        roles = userObj.roles
        #如果此帐号没有角色
        if len(roles) == 0:
            return True, roles

        #待拼接返回给用户的权限dict
        tempGroupAuth = {}
        #循环获取此用户所有的角色信息
        for i in range(0,len(roles)):
            authList = roles[i].auths
            #循环获取此角色所有的权限
            for j in range(0, len(authList)):
                #如果还没有这个权限大类
                if not tempGroupAuth.get(authList[j].groupName, None):
                    tempGroupAuth[authList[j].groupName] = {}
                #如果还没有这个权限规则
                if not tempGroupAuth[authList[j].groupName].get(authList[j].authName, None):
                    #如果这个权限规则里没有这个规则，则添加
                    tempGroupAuth[authList[j].groupName][authList[j].authName] = {
                        'authName':authList[j].authName,
                        'groupName':authList[j].groupName,
                        'authUrl':authList[j].authUrl,
                        'isMenu':authList[j].isMenu,
                    }

        return True, tempGroupAuth

    #初始化管理员
    @staticmethod
    def initAdmin():
        #查找admin表中是否有管理员
        userObj = admin.query.first()
        #如果已经有管理员
        if userObj:
            return
        #如果没有管理员，则要初始化一个
        defaultPassword = hashlib.md5('admin'+app.config['ADMIN_PASSWORD_SALT']).hexdigest().upper()
        adminIns = admin({
            'admin':'admin',
            'password':defaultPassword
        })
        roleIns = role({
            'roleName':'管理员组',
            'roleTips':'管理员组角色',
        })
        #为角色增加权限
        authName = '管理员管理'
        #添加管理员权限
        roleIns.auths.append(auth({
            'authName':'管理员列表',
            'groupName':authName,
            'authUrl':'/admin/list',
            'isMenu':True,
        }))
        roleIns.auths.append(auth(
            {
            'authName':'管理员读取',
            'groupName':authName,
            'authUrl':'/admin/read',
            'isMenu':False,
        }))
        roleIns.auths.append(auth(
            {
            'authName':'管理员修改',
            'groupName':authName,
            'authUrl':'/admin/save',
            'isMenu':False,
        }))
        roleIns.auths.append(auth(
            {
            'authName':'管理员删除',
            'groupName':authName,
            'authUrl':'/admin/delete',
            'isMenu':False,
        }))

        #添加角色权限
        roleIns.auths.append(auth(
            {
            'authName':'角色管理',
            'groupName':authName,
            'authUrl':'/role/list',
            'isMenu':True,
        }))
        roleIns.auths.append(auth(
            {
            'authName':'角色读取',
            'groupName':authName,
            'authUrl':'/role/read',
            'isMenu':False,
        }))
        roleIns.auths.append(auth(
            {
            'authName':'角色修改',
            'groupName':authName,
            'authUrl':'/role/save',
            'isMenu':False,
        }))
        roleIns.auths.append(auth(
            {
            'authName':'角色删除',
            'groupName':authName,
            'authUrl':'/role/delete',
            'isMenu':False,
        }))

        #添加权限管理权限
        roleIns.auths.append(auth(
            {
            'authName':'权限管理',
            'groupName':authName,
            'authUrl':'/auth/list',
            'isMenu':True,
        }))
        roleIns.auths.append(auth(
            {
            'authName':'权限读取',
            'groupName':authName,
            'authUrl':'/auth/read',
            'isMenu':False,
        }))
        roleIns.auths.append(auth(
            {
            'authName':'权限修改',
            'groupName':authName,
            'authUrl':'/auth/save',
            'isMenu':False,
        }))
        roleIns.auths.append(auth(
            {
            'authName':'权限删除',
            'groupName':authName,
            'authUrl':'/auth/delete',
            'isMenu':False,
        }))

        roleIns.auths.append(auth(
            {
            'authName':'上传文件',
            'groupName':authName,
            'authUrl':'/upload/save',
            'isMenu':False,
        }))
        roleIns.auths.append(auth(
            {
            'authName':'删除文件',
            'groupName':authName,
            'authUrl':'/upload/delete',
            'isMenu':False,
        }))

        roleIns.auths.append(auth(
            {
            'authName':'编辑器读取目录',
            'groupName':authName,
            'authUrl':'/thumb/read',
            'isMenu':False,
        }))
        roleIns.auths.append(auth(
            {
            'authName':'编辑器删除文件',
            'groupName':authName,
            'authUrl':'/thumb/delete',
            'isMenu':False,
        }))
        roleIns.auths.append(auth(
            {
            'authName':'编辑器创建目录',
            'groupName':authName,
            'authUrl':'/thumb/save',
            'isMenu':False,
        }))
        roleIns.auths.append(auth(
            {
            'authName':'编辑器上传文件',
            'groupName':authName,
            'authUrl':'/thumb/upload',
            'isMenu':False,
        }))


        adminIns.roles.append(roleIns)
        #将修改提交到数据库
        db.session.add(adminIns)
        db.session.commit()

        log.info('admin init success')

    #检查用户是否登录，并且获取管理员的权限
    @staticmethod
    def authLogin(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            #判断是否登录
            if not session.get('adminId', None):
                return redirect(url_for('loginPage'))

            #获取管理员的信息
            adminIns = adminBl()
            adminIns.adminId = session.get('adminId')
            ok1, adminObj = adminIns.getAdminById()
            ok2, adminAuth = adminIns.getAdminAuth()

            #如果没查询出错
            if not ok1 or not ok2:
                return redirect(url_for('loginOut'))

            reqPath = request.path
            hasAuth = False

            #如果访问首页，则直接授权
            homeUrl = url_for('homeIndex')
            if reqPath.find(homeUrl.decode()) >= 0:
                hasAuth = True
            #否则访问其他路径，判断权限
            else:
                for groupName in adminAuth:
                    for authName in adminAuth[groupName]:
                        if reqPath.find(adminAuth[groupName][authName]['authUrl']) >= 0:
                            hasAuth = True

            #如果没有访问权限，则报错
            if not hasAuth:
                return render_template('errorPage.html', errorTitle=u'403 您没有权限'), 403

            #将admin写入g对象
            g.admin = adminObj
            g.auth = adminAuth
            #返回参数管理员类和管理员权限类
            return f(*args, **kwargs)

        return decorated_function

    #获取列表页
    def getList(self):
        return self.getData()



    #添加或者更新一个管理员信息
    def saveOne(self):

        return self.saveData()

    #删除一个管理员
    def delOne(self):

        return self.delData()









