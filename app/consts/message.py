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


def reply_template(fr, to, time, reply):
    return REPLY_STR % (fr, to, time, reply)
