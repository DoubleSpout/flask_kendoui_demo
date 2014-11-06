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
from kendo.bussiness.UtilsBl import Utils
from kendo.bussiness.loginBl import adminBl

@adminBl.authLogin
def list():
    return render_template('index.html')


