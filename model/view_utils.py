import base64
import json
import os
import hashlib
import re
import tempfile
from tempfile import TemporaryFile
import matplotlib.image as mpimg
from flask import jsonify
from qiniu import Auth, put_file, etag, put_data, BucketManager, CdnManager
import qiniu.config

url_global = "http://pugtu5q13.bkt.clouddn.com/"


def check_phone(str):
    if len(str) != 11:
        return False
    elif str[0] != "1":
        return False
    # elif str[1:3] != "39" and str[1:3] != "31":
    #     # print(str[1:3])
    #     return False
    for i in range(3, 11):
        # print(str[i])
        if str[i] < "0" or str[i] > "9":
            return False
    return True


def error(str):
    data = {'code': 500, 'msg': str, 'data': None}
    return json.dumps(data, ensure_ascii=False)


def error2(str, type):
    if type == 'app':
        data = {'code': 500, 'msg': str, 'data': None}
        return json.dumps(data, ensure_ascii=False)
    elif type == 'web':
        data = {'msg': str}
        return jsonify(**data)
    else:
        data = {'code': 500, 'msg': str, 'data': None}
        return json.dumps(data, ensure_ascii=False)


def successful(type, str, **data):
    if type == 'app':
        data = {'code': 200, 'msg': str, 'data': data}
        return json.dumps(data, ensure_ascii=False)
    elif type == 'web':
        data = {'code': 200, 'msg': str, 'data': data}
        return jsonify(**data)


def judge(**dd):
    for a, b in dd.items():
        if not b:
            return False
    return True


def up_image(id, type, image):
    # 需要填写你的 Access Key 和 Secret Key
    access_key = 'AyFlrr-Ijdy2wHCbeSorUTtZIRHDsAsw8oVg1pza'
    secret_key = 'fqzX7_YSR70ETJsay5mil1vjyiJbak_uqKcZ8L9X'
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = 'nese'
    # 上传后保存的文件名
    key = type + id + '.png'
    # 上传文件到七牛后， 七牛将文件名和文件大小回调给业务服务器。
    policy = {
        'callbackUrl': 'http://pugtu5q13.bkt.clouddn.com/callback.php',
        'callbackBody': 'filename=$(fname)&filesize=$(fsize)'
    }
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)
    # 要上传文件的本地路径
    localfile = image

    ret, info = put_data(token, key, localfile)
    # print(info)
    # assert ret['key'] == key
    # assert ret['hash'] == etag(localfile)


def up_image(id, param, type, image):
    # 需要填写你的 Access Key 和 Secret Key
    access_key = 'AyFlrr-Ijdy2wHCbeSorUTtZIRHDsAsw8oVg1pza'
    secret_key = 'fqzX7_YSR70ETJsay5mil1vjyiJbak_uqKcZ8L9X'
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = 'nese'
    # 上传后保存的文件名
    key = type + id + param + '.png'
    # 上传文件到七牛后， 七牛将文件名和文件大小回调给业务服务器。
    policy = {
        'callbackUrl': 'http://pugtu5q13.bkt.clouddn.com/callback.php',
        'callbackBody': 'filename=$(fname)&filesize=$(fsize)'
    }
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)
    # 要上传文件的本地路径
    localfile = image

    ret, info = put_data(token, key, localfile)


def delete_image(id, type):
    access_key = 'AyFlrr-Ijdy2wHCbeSorUTtZIRHDsAsw8oVg1pza'
    secret_key = 'fqzX7_YSR70ETJsay5mil1vjyiJbak_uqKcZ8L9X'
    q = Auth(access_key, secret_key)
    bucket = BucketManager(q)
    bucket_name = 'nese'
    key = type + id + '.png'
    bucket.delete(bucket_name, key)


def refresh_image(id, type):
    access_key = 'AyFlrr-Ijdy2wHCbeSorUTtZIRHDsAsw8oVg1pza'
    secret_key = 'fqzX7_YSR70ETJsay5mil1vjyiJbak_uqKcZ8L9X'
    auth = qiniu.Auth(access_key=access_key, secret_key=secret_key)
    cdn_manager = CdnManager(auth)
    urls = [url_global + type + id + '.png']
    print(urls)
    refresh_url_result = cdn_manager.refresh_urls(urls)


def get_id(str):
    sub_str = str.split('/')[-1]
    pattern = re.compile(r'\d+')
    id = int(pattern.findall(sub_str)[0])
    return id


# if __name__ == '__main__':
#     get_id('http://pugtu5q13.bkt.clouddn.com/user12350.png')