import unittest
from unittest import TestCase
import requests
from app.view.wechat import *


class AnswerMsgTestCase (TestCase):
    def setUp(self):
        self.url = 'https://chatterbot.yuanw.wang/api/wx/'
        self.headers = {'Content-Type': 'text/xml'}

    def test_answer_text_msg(self):
        datas = '''<xml>
                <ToUserName><![CDATA[toUser]]></ToUserName>
                <FromUserName><![CDATA[fromUser]]></FromUserName>
                <CreateTime>1348831860</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[???]]></Content>
                <MsgId>1234567890123456</MsgId>
                </xml>'''
        r = requests.post(url=self.url, data=datas, headers=self.headers)
        self.assertEqual(r.status_code, 200)

    def test_answer_other_msg(self):

        image_data = '''<xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>1348831860</CreateTime>
        <MsgType><![CDATA[image]]></MsgType>
        <PicUrl><![CDATA[this is a url]]></PicUrl>
        <MediaId><![CDATA[media_id]]></MediaId>
        <MsgId>1234567890123456</MsgId>
        </xml>'''

        video_data = '''<xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>1357290913</CreateTime>
        <MsgType><![CDATA[video]]></MsgType>
        <MediaId><![CDATA[media_id]]></MediaId>
        <ThumbMediaId><![CDATA[thumb_media_id]]></ThumbMediaId>
        <MsgId>1234567890123456</MsgId>
        </xml>'''
        shortv_data = '''<xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>1357290913</CreateTime>
        <MsgType><![CDATA[shortvideo]]></MsgType>
        <MediaId><![CDATA[media_id]]></MediaId>
        <ThumbMediaId><![CDATA[thumb_media_id]]></ThumbMediaId>
        <MsgId>1234567890123456</MsgId>
        </xml>'''
        location_data = '''<xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>1351776360</CreateTime>
        <MsgType><![CDATA[location]]></MsgType>
        <Location_X>23.134521</Location_X>
        <Location_Y>113.358803</Location_Y>
        <Scale>20</Scale>
        <Label><![CDATA[location]]></Label>
        <MsgId>1234567890123456</MsgId>
        </xml>'''
        link_data = '''<xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>1351776360</CreateTime>
        <MsgType><![CDATA[link]]></MsgType>
        <Title><![CDATA[link]]></Title>
        <Description><![CDATA[link]]></Description>
        <Url><![CDATA[url]]></Url>
        <MsgId>1234567890123456</MsgId>
        </xml>'''
        datas = [image_data, shortv_data, video_data, location_data, link_data]

        for d in datas:
            r = requests.post(url=self.url, data=d, headers=self.headers)
            xml_rec = et.fromstring(r.text)
            self.assertEqual(r.status_code, 200)
            self.assertEqual(xml_rec.find('Content').text, '看不懂诶')

    def test_event_msg(self):
        sub_event_data = '''<xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>1348831860</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[subscribe]]></Event>
        <MsgId>1234567890123456</MsgId>
        </xml>'''
        unsub_event_data = '''<xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>1348831860</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[unsubscribe]]></Event>
        <MsgId>1234567890123456</MsgId>
        </xml>'''

        r = requests.post(url=self.url, data=sub_event_data,
                          headers=self.headers)
        xml_rec = et.fromstring(r.text)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(xml_rec.find('Content').text, '你好哇，我是WeChatterBot!')

        r = requests.post(url=self.url, data=unsub_event_data,
                          headers=self.headers)
        xml_rec = et.fromstring(r.text)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(xml_rec.find('Content').text, '再见，有空再来找我玩~')

    def test_voice_msg(self):
        voice_data = '''<xml>
        <ToUserName><![CDATA[toUser]]></ToUserName>
        <FromUserName><![CDATA[fromUser]]></FromUserName>
        <CreateTime>1357290913</CreateTime>
        <MsgType><![CDATA[voice]]></MsgType>
        <MediaId><![CDATA[media_id]]></MediaId>
        <Format><![CDATA[Format]]></Format>
        <MsgId>1234567890123456</MsgId>
        </xml>'''

        r = requests.post(url=self.url, data=voice_data, headers=self.headers)
        xml_rec = et.fromstring(r.text)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(xml_rec.find('Content').text, '风太大听不清还是用文字跟我聊天吧>.<')

    def test_lack_key(self):
        # 明文模式
        data_lack_type = '''<xml>
                <ToUserName><![CDATA[toUser]]></ToUserName>
                <FromUserName><![CDATA[fromUser]]></FromUserName>
                <CreateTime>1348831860</CreateTime>
                <Content><![CDATA[???]]></Content>
                <MsgId>1234567890123456</MsgId>
                </xml>'''
        data_lack_content = '''<xml>
                <ToUserName><![CDATA[toUser]]></ToUserName>
                <FromUserName><![CDATA[fromUser]]></FromUserName>
                <CreateTime>1348831860</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <MsgId>1234567890123456</MsgId>
                </xml>'''
        datas = [data_lack_type, data_lack_content]
        for d in datas:
            r = requests.post(url=self.url, data=d, headers=self.headers)
            self.assertEqual(r.status_code, 400)
            self.assertEqual(r.text, '{"error": "参数不正确", "code": 10000001}')

        # 密文模式
        param = {'signature': 'signature', 'timestamp': 'timestamp',
                 'nonce': 'nonce', 'encrypt_type': 'aes'}
        r = requests.post(url=self.url, params=param,
                          data=data_lack_type, headers=self.headers)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.text, '{"error": "参数不正确", "code": 10000001}')

    def test_cryptor(self):

        data = '''<xml><ToUserName><![CDATA[gh_10f6c3c3ac5a]]></ToUserName><FromUserName><![CDATA[oyORnuP8q7ou2gfYjqLzSIWZf0rs]]></FromUserName><CreateTime>1409735668</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[abcdteT]]></Content><MsgId>6054768590064713728</MsgId><Encrypt><![CDATA[hyzAe4OzmOMbd6TvGdIOO6uBmdJoD0Fk53REIHvxYtJlE2B655HuD0m8KUePWB3+LrPXo87wzQ1QLvbeUgmBM4x6F8PGHQHFVAFmOD2LdJF9FrXpbUAh0B5GIItb52sn896wVsMSHGuPE328HnRGBcrS7C41IzDWyWNlZkyyXwon8T332jisa+h6tEDYsVticbSnyU8dKOIbgU6ux5VTjg3yt+WGzjlpKn6NPhRjpA912xMezR4kw6KWwMrCVKSVCZciVGCgavjIQ6X8tCOp3yZbGpy0VxpAe+77TszTfRd5RJSVO/HTnifJpXgCSUdUue1v6h0EIBYYI1BD1DlD+C0CR8e6OewpusjZ4uBl9FyJvnhvQl+q5rv1ixrcpCumEPo5MJSgM9ehVsNPfUM669WuMyVWQLCzpu9GhglF2PE=]]></Encrypt></xml>'''

        invalid_param = {'signature': '4dbdbe7c66c7d80b6b2b59e138a58484f915256b', 'timestamp': '1409735669',
                         'msg_signature': '2222222ffba7e9b25a30732f161a50dee', 'nonce': '1320562132', 'encrypt_type': 'aes'}

        # 加解密失败
        r = requests.post(url=self.url, params=invalid_param,
                          data=data, headers=self.headers)
        self.assertEqual(r.status_code, 400)
        # self.assertEqual(r.text, '{"error": "消息加密失败", "code": 10000031}')


if __name__ == '__main__':
    unittest.main()
