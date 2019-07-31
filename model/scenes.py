import random

from flask import Blueprint, request, render_template, flash

from exts import db
from model.view_utils import *
from models import Dialogue

scene_manage = Blueprint("scene", __name__)


@scene_manage.route('/scene/<int:sid><int:page>', methods=['GET', 'POST'])
def scene(sid,page):
    if request.method == 'GET':
        dialogues = Dialogue.query.filter(Dialogue.dsid == sid).paginate(page=page, per_page=6)
        return render_template('scene.html', dialogues=dialogues,sid=sid)


@scene_manage.route('/delete_dialogue/<int:sid><int:page>', methods=['GET', 'POST'])
def delete_dialogue(sid, page):
    if request.method == 'POST':
        type = request.values.get('type')
        msg = request.values.to_dict()
        if not judge(**msg):
            return error2("请求参数缺失", type)
        did = request.values.get('did')
        dialogue = Dialogue.query.fliter(Dialogue.did == did).first()
        if not dialogue:
            return error2("此会话不存在", type)
        db.session.delete(dialogue)
        db.session.commit()
        data = {}
        return successful(type, "删除对话成功", **data)


@scene_manage.route('/add_dialogue/', methods=['GET', 'POST'])
def add_dialogue():
    if request.method == 'GET':
        sid = request.values.get('sid')
        # page = request.values.get('page')
        # print('page',page)
        # print(request.values)
        return render_template('add_dialogue.html', sid=sid)
    else:
        type = request.values.get('type')
        msg = request.values.to_dict()
        if not judge(**msg):
            return error2("请求参数缺失", type)
        dname = request.values.get('dname')
        msg = Dialogue.query.all()[-1]
        did = msg.did + random.randint(1, 10)
        durl = request.values.get('durl')
        dlyric = request.values.get('dlyric')
        dsid = request.values.get('dsid')
        dialogue = Dialogue(did=did, dname=dname, dlyric=dlyric, durl=durl, dsid=dsid)
        db.session.add(dialogue)
        db.session.commit()
        data = {}
        # return successful(type,"添加文章成功",**data)
        flash("添加文章成功")
        return render_template('add_dialogue.html', sid=dsid)


# @scenes_manage.route('/add_dialogue/', methods=['POST'])
# def add_dialogue():

