import json
import random

from flask import Blueprint, request, render_template, flash, jsonify
from model.view_utils import *
from exts import db
from models import Passage, User, Collection

passage_manage = Blueprint("passage", __name__)


@passage_manage.route('/get_all/', methods=['GET', 'POST'])
def get_all():
    if request.method == 'GET':
        type = request.values.get('type')
        msg = request.values.to_dict()
        if not judge(**msg):
            return error2('请求参数缺失', type)
        page_size = request.values.get('page_size')
        page_num = request.values.get('page_num')
        passage = Passage.query.paginate(page_num, page_size)
        total = passage.total
        msg = []
        for item in passage:
            msg.append({'pid': item.pid, 'ptitle': item.ptitle, 'ppic': item.ppic, 'purl': item.purl})
        msg = {'total': total, 'list': msg}
        return successful(type, "文章列表如下", **msg)


@passage_manage.route('/get_collection/', methods=['GET', 'POST'])
def get_collection():
    if request.method == 'GET':
        msg = request.values.to_dict()
        if not judge(**msg):
            return error('请求参数缺失')
        id = request.values.get('id')
        password = request.values.get('password')
        user = User.query.filter(User.id == id, User.password == password).first()
        if not user:
            return error('用户id或密码不正确')
        else:
            if request.values.get('type') == 'app':
                msg = []
                collection = Collection.query.filter(Collection.cid == id).all()
                for item in collection:
                    passage = Passage.query.filter(Passage.cpid == item.cpid).first()
                    msg.append({'pid': passage.pid, 'ptitle': passage.ptitle, 'ppic': passage.ppic, 'purl': passage.purl})
                data = {'code': 200, 'msg': '成功返回用户收藏的文章', 'data': msg}
                return json.dumps(data, ensure_ascii=False)


@passage_manage.route('/add_collection/', methods=['GET', 'POST'])
def add_collection():
    if request.method == 'POST':
        type = request.values.get('type')
        msg = request.values.to_dict()
        if not judge(**msg):
            return error2('请求参数缺失', type)
        cid = int(request.values.get('cid'))
        # password = request.values.get('password')
        # password = base64.b64encode(bytes(password, "utf-8"))
        user = User.query.filter(User.id == cid).first()
        if not user:
            return error2('用户名或密码不正确', type)
        cpid = int(request.values.get('cpid'))
        date = request.values.get('date')
        # passage = Passage.query.filter(Passage.pid == pid).first()
        collection = Collection(cpid=cpid, cid=cid, date=date)
        db.session.add(collection)
        db.session.commit()
        data = {}
        return successful(type, '成功收藏文章', **data)
    else:
        return render_template('add_collection.html')


@passage_manage.route('/cancel_collection/', methods=['GET', 'POST'])
def cancel_collection():
    if request.method == 'POST':
        type = request.values.get('type')
        msg = request.values.to_dict()
        if not judge(**msg):
            return error('请求参数缺失')
        cid = int(request.values.get('cid'))
        # password = request.values.get('password')
        # user = User.query.filter(User.id == cid).first()
        #         # if not user:
        #         #     return error('用户名或密码不正确')
        cpid = int(request.values.get('cpid'))
        date = request.values.get('date')
        print(request.values)
        collection = Collection.query.filter(Collection.cid == cid, Collection.cpid == cpid, Collection.date == date).first()
        if not collection:
            return error2('未收藏此文章',type)
        db.session.delete(collection)
        db.session.commit()
        data = {}
        return successful(type, "取消收藏成功", **data)


@passage_manage.route("/add_passage/",methods=['GET', 'POST'])
def add_passage():
    if request.method == 'POST':
        type = request.values.get('type')
        msg = request.values.to_dict()
        if not judge(**msg):
            return error2('请求参数缺失', type)
        ptitle = request.values.get('ptitle')
        purl = request.values.get('purl')
        ppic = request.files.get('ppic')
        if not ppic:
            return error2('图片数据缺失', type)
        msg = Passage.query.all()[-1]
        pid = msg.pid + random.randint(1, 10)
        ppic = ppic.read()
        type_passage = 'passage'
        param = '/0'
        up_image(str(pid),param, type, ppic)
        ppic = url_global + type_passage + str(pid) + param + '.png'
        passage = Passage(pid=pid,ptitle=ptitle, purl=purl, ppic=ppic)
        db.session.add(passage)
        db.session.commit()
        flash("添加文章成功")
        data = {}
        return successful(type, "添加文章成功", **data)

    else:
        return render_template('add_passage.html')


@passage_manage.route('/delete_passage/', methods=['GET', 'POST'])
def delete_passage():
    if request.method == 'POST':
        type = request.values.get('type')
        msg = request.values.to_dict()
        if not judge(**msg):
            return error2("请求参数缺失", type)
        pid = request.values.get('pid')
        passage = Passage.query.filter(Passage.pid == pid).first()
        collection = Collection.query.filter(Collection.cpid == pid).all()
        if not passage:
            return error2("该文章不存在", type)
        else:
            db.session.delete(passage)
            for item in collection:
                db.session.delete(item)
            db.session.commit()
            data = {}
            return successful(type, "成功删除文章", **data)


@passage_manage.route('/query_passage/', methods=['GET', 'POST'])
def query_passage():
    if request.method == 'POST':
        type = request.values.get('type')
        msg = request.values.to_dict()
        if not judge(**msg):
            return error2("请求参数缺失", type)
        pid = request.values.get('pid')
        passage = Passage.query.filter(Passage.pid == pid).first()
        if not passage:
            return error2("该文章不存在", type)
        else:
            data = {'pid': passage.pid, 'ptitle': passage.ptitle, 'ppic': passage.ppic, 'purl': passage.purl}
            return successful(type, "查询文章成功", **data)

