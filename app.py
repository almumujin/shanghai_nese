import base64

import flask
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_wtf import form
import matplotlib.pyplot as plt
import json
from config import DevConfig
from model.discover import passage_manage
from model.view_utils import judge
from models import User, Message, Passage, Collection, Scene
from exts import db
from functools import wraps
from model.users import user_manage
from model.scenes import scene_manage

app = Flask(__name__)
app.config.from_object(DevConfig)
db.init_app(app)
app.register_blueprint(user_manage, url_prefix='/manage/user_manage')
app.register_blueprint(passage_manage, url_prefix='/manage/passage_manage')
app.register_blueprint(scene_manage, url_prefix='/manage/scene_manage')


# 登录限制的装饰器
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user_id'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))

    return wrapper


@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        message = Message.query.filter(Message.telephone == telephone, Message.password == password).first()
        if message:
            session['user_id'] = message.id
            # 如果需31天免登录
            # session.permanent = True
            return redirect(url_for('index'))
        else:
            return '手机号或者密码错误'


@app.route('/regist/', methods=['GET', 'POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # 手机号码验证
        message = Message.query.filter(Message.telephone == telephone).first()
        # print(user)
        if message:
            return '该手机号码已被注册'
        else:
            if password1 != password2:
                return '两次密码不一致'
            else:
                message = Message(telephone=telephone, username=username, password=password1)
                db.session.add(message)
                db.session.commit()
                return render_template('login.html')


@app.route('/logout/')
def logout():
    # session.pop('user_id')
    # del session['user_id']
    session.clear()
    return redirect(url_for('login'))


@app.route('/manage/', methods=['GET', 'POST'])
@login_required
def manage():
    if request.method == 'GET':
        return render_template('user_manage.html')
    else:
        pass


@app.route('/manage/user_manage/<int:page>', methods=['GET', 'POST'])
@login_required
def user_manage(page):
    if request.method == 'GET':
        if not page:
            page = 1
        users = User.query.paginate(page=page, per_page=5)
        user = users.items[0]
        user.password = base64.b64decode(bytes(user.password, "utf-8"))
        user.password = user.password.decode('utf-8')
        return render_template('user_manage.html', users=users, user=user)

#
# @app.route('/manage/passage_manage/', methods=['GET', 'POST'])
# @login_required
# def ():
#     if request.method == 'GET':
#         return render_template('passage_manage.html')
#     else:
#         pass


@app.route('/manage/passage_manage/<int:page1><int:page2>', methods=['GET', 'POST'])
@login_required
def passage_manage(page1, page2):
    if request.method == 'GET':
        if not page1:
            page1 = 1
        if not page2:
            page2 = 1
        passages = Passage.query.paginate(page=page2, per_page=9)
        collections = Collection.query.paginate(page=page1, per_page=8)
        users = []
        for item in collections.items:
            user = User.query.filter(User.id == item.cid).first()
            users.append(user)
        return render_template('passage_manage.html',passages=passages,collections=collections,users=users)
    else:
        pass


@app.route('/manage/scene_manage/', methods=['GET', 'POST'])
@login_required
def scene_manage():
    if request.method == 'GET':
        scenes = Scene.query.all()
        return render_template('scene_manage.html', scenes=scenes)


@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        message = Message.query.filter(Message.id == user_id).first()
        if message:
            return {'message': message}
    return {}


if __name__ == '__main__':
    app.run()
