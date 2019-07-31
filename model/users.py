import base64
import json
import os
import random
import re

import flask

from model.view_utils import *
from flask import Blueprint, request, render_template, app, redirect, url_for, flash, jsonify, g
# from app import app
from exts import db
from models import User
user_manage = Blueprint("users", __name__)


@user_manage.route('/add_user/', methods=['GET', "POST"])
def add_user():
    if request.method == 'GET':
        return redirect(url_for('user_manage'))
    else:
        msg = request.values.to_dict()
        if not judge(**msg):
            error_msg = 'POST提交参数缺失'
            return error(error_msg)
        head_image = request.files.get('head_image')
        if not head_image:
            error_msg = '头像数据缺失'
            return error(error_msg)
        username = request.values.get('username')
        if len(username) > 6:
            return error('用户名长度必须小于6')
        user = User.query.filter(User.username == username).first()
        if user:
            error_msg = '用户名已存在'
            return error(error_msg)
        telephone = request.values.get('telephone')
        if not check_phone(telephone):
            return error('手机号错误')
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return error('该手机号码已被注册')
        password = request.values.get('password')
        if len(password) > 12:
            return error('密码长度必须小于12')
        sex = int(request.values.get('sex'))
        if sex not in [0, 1]:
            return error('性别必须为0或1')
        msg = User.query.all()[-1]
        if msg:
            id = msg.id + random.randint(1, 10)
        else:
            id = 12345
        head_image = head_image.read()
        type = 'user'
        param = '/0'
        up_image(str(id), param, type, head_image)
        image_url = url_global + type + str(id) + param + '.png'
        head_image = image_url
        password = base64.b64encode(bytes(password, "utf-8"))
        nickname = request.values.get('nickname')
        user = User(id=id, username=username, telephone=telephone, password=password, head_image=head_image, sex=sex, nickname=nickname)
        db.session.add(user)
        db.session.commit()
        if request.values.get('type') == 'app':
            data = {'code': 200, 'msg': '注册成功', 'data': None}
            return json.dumps(data, ensure_ascii=False)
        else:
            flash("添加用户成功")
            return redirect(url_for('user_manage'))


@user_manage.route('/query_user/', methods=['GET', 'POST'])
def query_user():
    if request.method == 'POST':
        msg = request.values.to_dict()
        if not judge(**msg):
            data = {'code': 500, 'msg': 'POST提交参数缺失', 'data': None}
            return json.dumps(data, ensure_ascii=False)
        username = request.values.get('username')
        user = User.query.filter(User.username == username).first()
        if user:
            flash('查询用户成功')
            if user.sex == 1:
                sex = '男'
            else:
                sex = '女'
            user = {'id': user.id, 'username': user.username, 'telephone': user.telephone,
                     'password': user.password, 'head_image': user.head_image, 'sex': sex}
            return flask.jsonify(**user)
        else:
            flash('该用户不存在')
            return ""
    if request.method == 'GET':
        return redirect(url_for('user_manage'))


@user_manage.route('/user/login/', methods=['GET', 'POST'])
def return_msg():
    if request.method == 'GET':
        msg = request.values.to_dict()
        if not judge(**msg):
            data = {'code': 500, 'msg': '请求参数缺失', 'data': None}
            return json.dumps(data, ensure_ascii=False)
        username = request.values.get('username')
        password = request.values.get('password')
        password = base64.encode(password)
        user = User.query.filter(User.username == username, User.password == password).first()
        user.password = base64.b64decode(password).decode()
        if user:
            data = {'code': 200, 'msg': '成功返回用户信息', 'data': {'id': user.id, 'username': user.username, 'telephone': user.telephone,
                                                         'nickname': user.nickname, 'head_image': user.head_image, 'sex': user.sex}}
            return json.dumps(data, ensure_ascii=False)
        else:
            return error('账号或密码错误')


@user_manage.route('/delete_user/', methods=['POST'])
def delete_user():
    if request.method == 'POST':
        pass


@user_manage.route('/modify_user_message/<int:id><int:page>', methods=['GET', 'POST'])
def modify_user_message(id, page):
    if request.method == 'POST':
        type = request.values.get('type')
        msg = request.values.to_dict()
        if not judge(**msg):
            return error("请求参数缺失")
        username = request.values.get('username')
        if len(username) > 6:
            return error('用户名长度必须小于6')
        sex = request.values.get('sex')
        if sex == '男':
            sex = 1
        else:
            sex = 0
        if int(sex) not in [0, 1]:
            return error('性别必须为0或1')
        nickname = request.values.get('nickname')
        password = request.values.get('password')
        if len(password) > 12:
            return error('密码长度必须小于12')
        telephone = request.values.get('telephone')
        if not check_phone(telephone):
            return error('手机号错误')
        user2 = User.query.filter(User.username == username).first()
        user = User.query.filter(User.id == id).first()
        users = User.query.paginate(page=page, per_page=5)
        if user2:
            user2.sex = sex
            user2.nickname = nickname
            user2.password = password
            user2.password = base64.b64encode(bytes(user2.password, "utf-8"))
            user2.telephone = telephone
            db.session.commit()
            user.password = base64.b64decode(bytes(user.password, "utf-8"))
            user.password = user.password.decode('utf-8')
            flash("修改用户信息成功")
            return render_template('user_manage.html', user=user, users=users)
        else:
            head_image = url_global + "profile-image.png"
            password = base64.b64encode(bytes(password, "utf-8"))
            user3 = User(username=username, password=password, sex=sex, nickname=nickname, head_image=head_image, telephone=telephone)
            db.session.add(user3)
            db.session.commit()
            flash("添加用户成功")
            user.password = base64.b64decode(bytes(user.password, "utf-8"))
            user.password = user.password.decode('utf-8')
            return render_template('user_manage.html', user=user, users=users)


@user_manage.route('/get_user/<int:id><int:page>', methods=['GET', 'POST'])
def get_user(id, page):
    if request.method == 'GET':
        user = User.query.filter(User.id == id).first()
        user.password = base64.b64decode(bytes(user.password, "utf-8"))
        user.password = user.password.decode('utf-8')
        users = User.query.paginate(page=page, per_page=5)
        return render_template('user_manage.html', user=user, users=users)


@user_manage.route('/modify_image/', methods=['GET', 'POST'])
def modify_image():
    if request.method == 'POST':
        type = request.values.get('type')
        msg = request.values.to_dict()
        if not judge(**msg):
            return error2("请求参数缺失", type)
        id = request.values.get('id')
        head_image = request.files.get('head_image')
        if not head_image:
            return error2("请提交修改头像", type)
        head_image = head_image.read()
        user = User.query.filter(User.id == id).first()
        if not user:
            return error2("提交数据缺失", type)
        type_image = 'user'
        tmp = get_id(user.head_image)
        param = '/' + str(tmp+1)
        up_image(str(user.id), param, type_image,  head_image)
        new_url = url_global + type_image + id + param + '.png'
        user.head_image = new_url
        db.session.commit()
        if type == 'web':
            data = {'msg': "修改头像成功", 'head_image': user.head_image}
            return jsonify(**data)
        # return render_template('user_manage.html', user=user, users=users)



# if __name__ == '__main__':
#     print(check_phone('12345678888'))