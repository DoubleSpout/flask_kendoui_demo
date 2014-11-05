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
from flask import render_template, request, redirect, url_for, sessions, Response, session
from sqlalchemy import *
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import load_only, joinedload, dynamic_loader, lazyload, defer, undefer
from sqlalchemy.ext.serializer import loads, dumps
from kendo import app
from kendo import config
from kendo.models.adminModel import *
from kendo.models.roleModel import *
from kendo.models.authModel import *
from kendo.bussiness.LoggerBl import log
from kendo.models.dbModel import db



class adminBl(object):

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
            return false, '未找到此管理员'
        postPassword = hashlib.md5(postPassword+config['ADMIN_PASSWORD_SALT']).hexdigest().upper()
        if postPassword != userObj.password:
            return false, '用户名密码错误'

        adminIns.sqlData = userObj
        return true, adminIns.dumpToList()

    #获取管理员信息方法
    def getAdminById(self):
        adminIns = admin()

        userObj = admin.query.filter_by(Id=self.adminId, isShow=True).first()
        if not userObj:
            return false, '未找到此管理员'

        adminIns.sqlData = userObj
        return true, adminIns.dumpToList()

    #获取管理员的权限方法
    def getAdminAuth(self):
        ok, userObj = self.getAdminById()
        if not ok:
            return ok, userObj

        roles = userObj.roles
        #如果此帐号没有角色
        if len(roles) == 0:
            return true, roles

        #待拼接返回给用户的权限dict
        tempGroupAuth = {}
        #循环获取此用户所有的角色信息
        for i in range(0,len(roles)):
            authList = roles[i].auths
            #循环获取此角色所有的权限
            for j in range(0, len(authList)):
                #如果还没有这个权限大类
                if not tempGroupAuth[authList[j].groupName]:
                    tempGroupAuth[authList[j].groupName] = {}
                #如果还没有这个权限规则
                if not tempGroupAuth[authList[j].groupName][authList[j].authName]:
                    #如果这个权限规则里没有这个规则，则添加
                    tempGroupAuth[authList[j].groupName][authList[j].authName] = {
                        'authName':authList[j].authName,
                        'groupName':authList[j].groupName,
                        'authUrl':authList[j].authUrl,
                        'isMenu':authList[j].isMenu,
                    }

        return true, tempGroupAuth

    #初始化管理员
    @staticmethod
    def initAdmin():
        #查找admin表中是否有管理员
        userObj = admin.query.first()
        #如果已经有管理员
        if userObj:
            return
        #如果没有管理员，则要初始化一个
        defaultPassword = hashlib.md5('admin'+config['ADMIN_PASSWORD_SALT']).hexdigest().upper()
        adminIns = admin('admin', defaultPassword)
        roleIns = role('管理员组', '管理员组角色')
        #为角色增加权限
        authName = '管理员管理'
        #添加管理员权限
        roleIns.auths.append(auth('管理员列表', authName, '/admin/list', True))
        roleIns.auths.append(auth('管理员读取', authName, '/admin/read'))
        roleIns.auths.append(auth('管理员修改', authName, '/admin/save'))
        roleIns.auths.append(auth('管理员删除', authName, '/admin/delete'))
        #添加角色权限
        roleIns.auths.append(auth('角色管理', authName, '/role/list', True))
        roleIns.auths.append(auth('角色读取', authName, '/role/read'))
        roleIns.auths.append(auth('角色修改', authName, '/role/save'))
        roleIns.auths.append(auth('角色删除', authName, '/role/delete'))
        #添加权限管理权限
        roleIns.auths.append(auth('权限管理', authName, '/auth/list', True))
        roleIns.auths.append(auth('权限读取', authName, '/auth/read'))
        roleIns.auths.append(auth('权限修改', authName, '/auth/save'))
        roleIns.auths.append(auth('权限删除', authName, '/auth/delete'))

        adminIns.roles.append(roleIns)
        #将修改提交到数据库
        db.session.add(adminIns)
        db.session.commit()

        log.info('admin init success')




    #添加或者更新一个管理员信息
    def saveOne(self):
        pass

    #删除一个管理员
    def delOne(self):
        pass

    #获取列表页
    def getList(self):
        pass







