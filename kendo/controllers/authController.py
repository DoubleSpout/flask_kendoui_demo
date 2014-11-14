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
from urlparse import parse_qsl, parse_qs
import urllib

from kendo.models.authModel import auth
from kendo.bussiness.UtilsBl import Utils
from kendo.bussiness.loginBl import adminBl
from kendo.bussiness.authBl import authBl

@adminBl.authLogin
def list():
    return render_template('authList.html')


@adminBl.authLogin
def read():
    objIns = authBl()
    objIns.modelClass = auth
    #获取原生的post字符串
    rawStr = urllib.unquote(request.stream.read())
    #设置参数
    objIns.kendoParam = rawStr

    #获取列表
    ok, result = objIns.getList()
    #如果出错
    if not ok:
        return render_template('errorPage.html', errotTitle=u'500 {0}'.format(result)), 500
    #返回json数据
    return Response(json.dumps(result), mimetype='application/json; charset=utf-8')


@adminBl.authLogin
def save():
    objIns = authBl()
    objIns.modelClass = auth
    #获取原生的post字符串
    rawStr = urllib.unquote(request.stream.read())
    #转换post字符串为dict，并赋值
    objIns.saveModel = rawStr
    ok, result = objIns.saveOne()
    #如果出错
    if not ok:
        return render_template('errorPage.html', errotTitle=u'500 {0}'.format(result)), 500
    #返回json数据
    return Response(json.dumps([result]), mimetype='application/json; charset=utf-8')


@adminBl.authLogin
def delete():
    objIns = authBl()
    objIns.modelClass = auth
    #获取原生的post字符串
    rawStr = urllib.unquote(request.stream.read())
    #转换post字符串为dict，并赋值
    objIns.delModel = rawStr
    #转换post字符串为dict，并赋值
    ok, result = objIns.delOne()
    #如果出错
    if not ok:
        return render_template('errorPage.html', errotTitle=u'500 {0}'.format(result)), 500
    #返回json数据
    return Response(json.dumps(result), mimetype='application/json; charset=utf-8')