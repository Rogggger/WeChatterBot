import time
import hashlib
import xml.etree.cElementTree as et

from flask import request, Blueprint

from app.consts.message import SIGNATURE_KEYS, MSG_KEYS, OTHER_MSG_TYPE, ENCRYPT_SIGNATURE_KEYS, reply_template
from app.consts.keys import WECHAT_TOKEN, WECHAT_APPID, WECHAT_AESKEY
from app.libs.msgcryptor import WXBizMsgCrypt

from app.libs.http import error_jsonify
from app.libs.chatbot import chatbot

bp_wechat = Blueprint('wx', __name__, url_prefix='/wx')


def check_signature(TOKEN, timestamp, nonce, signature):  # 签名验证
    lis = [TOKEN, timestamp, nonce]
    lis.sort()
    temp_str = "".join(lis).encode('utf-8')
    sign = hashlib.sha1(temp_str).hexdigest()
    return sign == signature


def get_reply(type, question):
    if type == 'text':
        response = chatbot.get_response(question)
        return response.text
    elif type == 'voice':
        return '风太大听不清还是用文字跟我聊天吧>.<'
    elif type == 'event':  # 事件推送的回复
        if question == 'subscribe':
            return '你好哇，我是WeChatterBot!在下方聊天框里输入中文和我聊天吧~'
        elif question == 'unsubscribe':
            return '再见，有空再来找我玩~'
        else:
            return '哈哈哈哈'
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

        if check_signature(WECHAT_TOKEN, req['timestamp'], req['nonce'],
                           req['signature']):
            return req['echostr']
        else:
            return error_jsonify(10000002)

    if request.method == 'POST':
        data = request.args
        encrypt_type = data.get('encrypt_type')
        if encrypt_type == 'aes':  # 加密模式
            req = {
                k: data[k]
                for k in ENCRYPT_SIGNATURE_KEYS if data.get(k) is not None
            }
            check_keys = ('signature', 'timestamp', 'nonce', 'msg_signature')
            if not all(k in req for k in check_keys):
                return error_jsonify(10000001)

            if not check_signature(WECHAT_TOKEN, req['timestamp'],
                                   req['nonce'], req['signature']):
                return error_jsonify(10000002)

            encrypt_content = request.get_data()
            wx_cryptor = WXBizMsgCrypt(WECHAT_TOKEN, WECHAT_AESKEY,
                                       WECHAT_APPID)  # 实例化加解密器对象
            ret, decrypt_xml = wx_cryptor.DecryptMsg(encrypt_content,
                                                     req['msg_signature'],
                                                     req['timestamp'],
                                                     req['nonce'])  # 解密
            if ret < 0:
                return error_jsonify(10000031)  # 解密失败
            xml_str = decrypt_xml
        else:  # 非加密模式
            xml_str = request.get_data()

        xml_rec = et.fromstring(xml_str)
        req_dic = {k: xml_rec.find(k) for k in MSG_KEYS}

        if req_dic['MsgType'] is None:
            return error_jsonify(10000001)
        if req_dic['MsgType'].text == 'event':
            req_dic['Content'] = xml_rec.find('Event')
        if req_dic['MsgType'].text in OTHER_MSG_TYPE:
            req_dic['Content'] = xml_rec.find('MsgType')
        if req_dic['Content'] is None:
            return error_jsonify(10000001)

        reply = get_reply(req_dic['MsgType'].text,
                          req_dic['Content'].text)  # 根据消息类型获得回复

        reply_xml = reply_template(req_dic['FromUserName'].text,
                                   req_dic['ToUserName'].text,
                                   int(time.time()), reply)
        if encrypt_type == 'aes':
            ret, encrypt_xml = wx_cryptor.EncryptMsg(reply_xml, req['nonce'])
            if ret < 0:
                return error_jsonify(10000032)  # 加密失败
            reply_xml = encrypt_xml
        return reply_xml
