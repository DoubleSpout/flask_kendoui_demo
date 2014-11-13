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
import werkzeug

from kendo import app
from kendo.models.adminModel import admin
from kendo.bussiness.UtilsBl import Utils
from kendo.bussiness.loginBl import adminBl


#@adminBl.authLogin
def save():
    file = request.files.get('upload_file', None)
    #检查格式
    ok, extName, saveFileName = Utils.checkAndGetExt(file, True)

    if not ok:
        return extName, 400
    #保存文件
    file.save(os.path.join(app.config.get('UPLOAD_FOLDER'), saveFileName))
    return Response(json.dumps({'result':'/static/upload/'+saveFileName}), mimetype='application/json; charset=utf-8')



@adminBl.authLogin
def delete():
    return Response(json.dumps({}), mimetype='application/json; charset=utf-8')
