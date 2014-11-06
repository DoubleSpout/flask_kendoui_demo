# -*- coding: utf-8 -*-
#coding=utf-8

#import package
import os
import flask
import json
from flask import flash, render_template, request, redirect, url_for, sessions, Response, session, make_response
import httplib
import urllib
from xml.dom.minidom import parse, parseString
from datetime import datetime
from kendo.bussiness.loginBl import *


def loginPage():
    #如果哟已经登录
    if session.get('adminId', None):
        return redirect(url_for('homeIndex'))

    return render_template('login.html', errorTips='')

def loginPost():
    admin = request.form.get('admin', None)
    password = request.form.get('password', None)
    adminBlIns = adminBl(admin, password)
    ok, result = adminBlIns.checkLogin()

    if not ok:
        #登录失败
        return render_template('login.html', errorTips=u'用户名或密码有误')
    else:
        #登录成功，写入session
        session['adminId'] = result.get('Id', None)
        return redirect(url_for('homeIndex'))

def loginOut():
    session['adminId'] = None
    return redirect(url_for('loginPage'))