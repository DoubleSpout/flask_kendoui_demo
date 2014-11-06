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


from kendo.bussiness.UtilsBl import Utils
from kendo.bussiness.loginBl import adminBl

@adminBl.authLogin
def list():
    return render_template('adminList.html')


@adminBl.authLogin
def read():
    adminIns = adminBl()
    #设置参数
    adminIns.kendoParam = request.form
    #将kendoui的参数解析为orm的参数
    adminIns.parseKendoData()
    #获取列表
    ok, result = adminIns.getList()
    #如果出错
    if not ok:
        return render_template('errorPage.html', errotTitle=u'500 {0}'.format(result)), 500
    #返回json数据
    return json.dumps(result)

@adminBl.authLogin
def save():
    adminIns = adminBl()
    adminIns.saveModel = request.form
    ok, result = adminIns.saveOne()
    #如果出错
    if not ok:
        return render_template('errorPage.html', errotTitle=u'500 {0}'.format(result)), 500
    #返回json数据
    return json.dumps([result])


@adminBl.authLogin
def delete():
    adminIns = adminBl()
    adminIns.delModel = request.form
    ok, result = adminIns.delOne()
    #如果出错
    if not ok:
        return render_template('errorPage.html', errotTitle=u'500 {0}'.format(result)), 500
    #返回json数据
    return json.dumps(result)