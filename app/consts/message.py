SIGNATURE_KEYS = ['signature', 'timestamp', 'nonce', 'echostr']
ENCRYPT_SIGNATURE_KEYS = ['signature', 'timestamp', 'nonce', 'msg_signature']
MSG_KEYS = ['ToUserName', 'FromUserName', 'MsgType', 'Content']
OTHER_MSG_TYPE = ['image', 'voice', 'video', 'shortvideo', 'location', 'link']

REPLY_STR = '''<xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[%s]]></Content>
                </xml>'''

WECHAT_TOKEN = 'gintoki'
WECHAT_APPID = 'wxaa4b38eec8c38711'
WECHAT_AESKEY = '4RysXPyaEFOF84d8zmh6VSNgwWztkTBXK3p22B7Ey7D'


def reply_template(fr, to, time, reply):
    return REPLY_STR % (fr, to, time, reply)
