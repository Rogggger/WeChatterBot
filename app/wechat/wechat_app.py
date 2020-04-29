from flask import Flask, request, abort, Blueprint
from time import time
import hashlib
import xml.etree.cElementTree as et
from app.wechat import msg_template as mt

wx_response = Blueprint('/api', __name__)

WECHAT_TOKEN = 'gintoki'
HOST = ''
app = Flask(__name__)


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
        signature = data.get('signature')
        timestamp = data.get('timestamp')
        nonce = data.get('nonce')
        echostr = data.get('echostr')
        req = {k: data.get(k) for k in mt.signature_key}
        if not all([req['signature'], req['timestamp'], req['nonce']]):
            abort(400)

        lis = [WECHAT_TOKEN, req['timestamp'], req['nonce']]
        lis.sort()
        temp_str = "".join(lis).encode('utf-8')

        sign = hashlib.sha1(temp_str).hexdigest()
        # print(sign)
        # 验证签名
        if req['signature'] != sign:
            abort(403)
        else:
            return req['echostr']

    if request.method == 'POST':
        xmldata = request.get_data()
        xml_rec = et.fromstring(xmldata)

        req = {k: xml_rec.find(k) for k in mt.msg_key}
        Content = get_reply(req['MsgType'], req['Content'])  # 根据信息类型获得回复

        return msg_template.reply_template(req['MsgType']) % (req['FromUserName'], req['ToUserName'], int(time()), req['Content'])


# if __name__ == '__main__':
#     # port:80
#     app.run(host=HOST, port=80, debug=True)
