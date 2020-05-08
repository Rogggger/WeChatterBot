SIGNATURE_KEYS = ['signature', 'timestamp', 'nonce', 'echostr']
MSG_KEYS = ['ToUserName', 'FromUserName', 'MsgType', 'Content']

REPLY_STR = '''<xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[%s]]></Content>
                </xml>'''

WECHAT_TOKEN = 'gintoki'


def reply_template(fr, to, time, reply):
    return REPLY_STR % (fr, to, time, reply)
