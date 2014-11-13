# -*- coding: utf-8 -*-
from flask import Flask, request
from kendo import app
from kendo.controllers import loginController, adminController, roleController, authController, homeController, \
    multiUploadController, editThumbController


#附件上传
app.add_url_rule('/upload/save', 'multiUploadSave', multiUploadController.save, methods=['POST'])
app.add_url_rule('/upload/delete', 'multiUploadRemove', multiUploadController.delete, methods=['POST'])

#文本编辑器上传和读取
app.add_url_rule('/thumb/read', 'thumbRead', editThumbController.read, methods=['POST'])
app.add_url_rule('/thumb/delete', 'thumbDelete', editThumbController.delete, methods=['POST'])
app.add_url_rule('/thumb/save', 'thumbSave', editThumbController.save, methods=['POST'])
app.add_url_rule('/thumb/upload', 'thumbUpload', editThumbController.upload, methods=['POST'])
app.add_url_rule('/thumb/get', 'thumbGet', editThumbController.get, methods=['GET'])


#登录的控制器
app.add_url_rule('/', 'index', loginController.loginPage, methods=['GET'])
app.add_url_rule('/login/page', 'loginPage', loginController.loginPage, methods=['GET'])
app.add_url_rule('/login/login', 'loginPost', loginController.loginPost, methods=['POST'])
app.add_url_rule('/login/logout', 'loginOut', loginController.loginOut, methods=['get'])
#首页
app.add_url_rule('/home/index', 'homeIndex', homeController.list, methods=['GET'])

#管理员路由
app.add_url_rule('/admin/list', 'adminList', adminController.list, methods=['GET'])
app.add_url_rule('/admin/read', 'adminRead', adminController.read, methods=['POST'])
app.add_url_rule('/admin/save', 'adminSave', adminController.save, methods=['POST'])
app.add_url_rule('/admin/delete', 'adminDelete', adminController.delete, methods=['POST'])

#角色路由
app.add_url_rule('/role/list', 'roleList', roleController.list, methods=['GET'])
app.add_url_rule('/role/read', 'roleRead', roleController.read, methods=['POST'])
app.add_url_rule('/role/save', 'roleSave', roleController.save, methods=['POST'])
app.add_url_rule('/role/delete', 'roleDelete', roleController.delete, methods=['POST'])

#权限路由
app.add_url_rule('/auth/list', 'authList', authController.list, methods=['GET'])
app.add_url_rule('/auth/read', 'authRead', authController.read, methods=['POST'])
app.add_url_rule('/auth/save', 'authSave', authController.save, methods=['POST'])
app.add_url_rule('/auth/delete', 'authDelete', authController.delete, methods=['POST'])