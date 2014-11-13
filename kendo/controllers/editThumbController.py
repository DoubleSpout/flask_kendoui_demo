# -*- coding: utf-8 -*-
#coding=utf-8

#import package
import os
import flask
import json
from flask import flash, render_template, request, redirect, url_for, sessions, Response, session, make_response, send_from_directory
import httplib
import urllib
import json
from xml.dom.minidom import parse, parseString
from datetime import datetime
from urlparse import parse_qsl, parse_qs
import urllib
import werkzeug

from kendo import app
from kendo.models.adminModel import admin
from kendo.bussiness.UtilsBl import Utils
from kendo.bussiness.loginBl import adminBl



def get():
    fileName = request.args.get('path', None)
    if not fileName:
        return 'empty path', 404

    return send_from_directory(app.config.get('UPLOAD_FOLDER'), fileName)


@adminBl.authLogin
def read():
    try:
        fileNameList = os.listdir(app.config.get('UPLOAD_FOLDER'))
        jsonList = []
        for item in fileNameList:
            jsonList.append({
                'name': item,
                'size': 0,
                'type': 'f'
            })
        return Response(json.dumps(jsonList), mimetype='application/json; charset=utf-8')

    except Exception as err:
        return err, 500



@adminBl.authLogin
def upload():
    file = request.files.get('file', None)
    #检查格式
    ok, extName, saveFileName = Utils.checkAndGetExt(file, True)
    if not ok:
        return extName, 400

    #保存文件
    file.save(os.path.join(app.config.get('UPLOAD_FOLDER'), saveFileName))
    return Response(json.dumps({
			'name': saveFileName,
			'size':0,
			'type':'f'
		}), mimetype='application/json; charset=utf-8')


@adminBl.authLogin
def save():
    #目前不支持
    return 'not support', 400



@adminBl.authLogin
def delete():
    filename = request.form.get('name', None)
    if not filename:
        return 'empty file name', 400

    try:
        os.remove(os.path.join(app.config.get('UPLOAD_FOLDER'), filename))
        return Response(json.dumps({}), mimetype='application/json; charset=utf-8')
    except Exception as err:
        return err, 500


