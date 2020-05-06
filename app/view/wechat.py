import time
import hashlib
import xml.etree.cElementTree as et

from flask import request, Blueprint

from app.consts.message import WECHAT_TOKEN, SIGNATURE_KEYS, MSG_KEYS, reply_template
from app.libs.http import error_jsonify

bp_wechat = Blueprint('wx', __name__,url_prefix='/wx')


def get_reply(type, question):
    if type == 'text':
        return question
    elif type == 'voice':
        return '风太大听不清还是用文字跟我聊天吧'
    elif type == 'event':
        return '来啦老弟欢迎关注'  # 订阅事件信息
    else:
        return '看不懂诶'


@bp_wechat.route('/', methods=['GET', 'POST'])
def wechat():
    if request.method == 'GET':
        data = request.args
        req = {k: data[k] for k in SIGNATURE_KEYS if data.get(k) is not None}
        check_keys = ('signature', 'timestamp', 'nonce')
        if not all(k in req for k in check_keys):
            return error_jsonify(10000001)

        lis = [WECHAT_TOKEN, req['timestamp'], req['nonce']]
        lis.sort()
        temp_str = "".join(lis).encode('utf-8')

        sign = hashlib.sha1(temp_str).hexdigest()

        if req['signature'] != sign:
            return error_jsonify(10000002)
        else:
            return req['echostr']

    if request.method == 'POST':
        xml_rec = et.fromstring(request.get_data())

        req = {k: xml_rec.find(k) for k in MSG_KEYS}
        reply = get_reply(req['MsgType'], req['Content'])  # 根据信息类型获得回复

        return reply_template(req['FromUserName'], req['ToUserName'], int(time.time()), reply)
