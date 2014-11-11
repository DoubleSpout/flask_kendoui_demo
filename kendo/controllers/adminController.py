# -*- coding: utf-8 -*-
#coding=utf-8

#import package
import os
import flask
import json
from flask import flash, render_template, request, redirect, url_for, sessions, Response, session, make_response
import httplib
import urllib
import json
from xml.dom.minidom import parse, parseString
from datetime import datetime
from formencode.variabledecode import variable_decode
from urlparse import parse_qsl, parse_qs
import urllib

from kendo.models.adminModel import admin
from kendo.bussiness.UtilsBl import Utils
from kendo.bussiness.loginBl import adminBl

@adminBl.authLogin
def list():
    return render_template('adminList.html')


@adminBl.authLogin
def read():
    adminIns = adminBl()
    adminIns.modelClass = admin
    #获取原生的post字符串
    rawStr = urllib.unquote(request.stream.read())
    #设置参数
    adminIns.kendoParam = rawStr

    #获取列表
    ok, result = adminIns.getList()
    #如果出错
    if not ok:
        return render_template('errorPage.html', errotTitle=u'500 {0}'.format(result)), 500
    #返回json数据
    return Response(json.dumps(result), mimetype='application/json; charset=utf-8')

@adminBl.authLogin
def save():
    adminIns = adminBl()
    adminIns.modelClass = admin
    #获取原生的post字符串
    rawStr = urllib.unquote(request.stream.read())
    #转换post字符串为dict，并赋值
    adminIns.saveModel = rawStr
    ok, result = adminIns.saveOne()
    #如果出错
    if not ok:
        return render_template('errorPage.html', errotTitle=u'500 {0}'.format(result)), 500
    #返回json数据
    return Response(json.dumps([result]), mimetype='application/json; charset=utf-8')


@adminBl.authLogin
def delete():
    adminIns = adminBl()
    adminIns.modelClass = admin
    #获取原生的post字符串
    rawStr = urllib.unquote(request.stream.read())
    #转换post字符串为dict，并赋值
    adminIns.delModel = rawStr
    #转换post字符串为dict，并赋值
    ok, result = adminIns.delOne()
    #如果出错
    if not ok:
        return render_template('errorPage.html', errotTitle=u'500 {0}'.format(result)), 500
    #返回json数据
    return Response(json.dumps(result), mimetype='application/json; charset=utf-8')