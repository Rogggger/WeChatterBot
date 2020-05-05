import time
import hashlib
import xml.etree.cElementTree as et

from flask import request, Blueprint

from app.wechat import msg_template as mt
from app.libs.http import error_jsonify

wx_response = Blueprint('/api', __name__)

WECHAT_TOKEN = 'gintoki'


def get_reply(type, question):
    if type == 'text':
        return question  # chatterbot_api
    elif type == 'voice':
        return '风太大听不清还是用文字跟我聊天吧'
    elif type == 'event':
        return '来啦老弟欢迎关注'  # 订阅事件信息
    else:
        return '看不懂诶'


@wx_response.route('/wx', methods=['GET', 'POST'])
def wechat():
    if request.method == 'GET':
        data = request.args
        req = {k: data[k] for k in mt.signature_key if data.get(k) is not None}
        check_keys = ('signature', 'timestamp', 'nonce')
        if not all(k in req for k in check_keys):
            error_jsonify(100001)

        lis = [WECHAT_TOKEN, req['timestamp'], req['nonce']]
        lis.sort()
        temp_str = "".join(lis).encode('utf-8')

        sign = hashlib.sha1(temp_str).hexdigest()

        if req['signature'] != sign:
            error_jsonify(100002)
        else:
            return req['echostr']

    if request.method == 'POST':
        xml_rec = et.fromstring(request.get_data())

        req = {k: xml_rec.find(k) for k in mt.msg_key}
        content = get_reply(req['MsgType'], req['Content'])  # 根据信息类型获得回复

        return mt.reply_template(req['MsgType']) % (
            req['FromUserName'], req['ToUserName'], int(time.time()), content)
