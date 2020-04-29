signature_key = ['signature', 'timestamp', 'nonce', 'echostr']
msg_key = ['ToUserName', 'FromUserName', 'MsgType', 'Content']

reply_str = '''<xml>
                <ToUserName>![CDATA[%s]]</ToUserName>
                <FromUserName>![CDATA[%s]]</FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType>![CDATA[text]]</MsgType>
                <Content>![CDATA[%s]]</Content>
                </xml>'''


def reply_template(type):
    if type == 'text':
        return reply_str
