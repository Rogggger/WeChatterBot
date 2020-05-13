import unittest
from unittest import TestCase
import requests
from app.view.wechat import *


class CheckSignatureTestCase (TestCase):

    def setUp(self):
        self.url = 'https://chatterbot.yuanw.wang/api/wx/'

    def test_valid_signature(self):
        r = requests.get(url=self.url, params={'timestamp': '1409735669', 'nonce': '1320562132',
                                               'signature': '4dbdbe7c66c7d80b6b2b59e138a58484f915256b', 'echostr': 'connected'})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.text, 'connected')

    def test_invalid_signature(self):
        r = requests.get(url=self.url, params={'timestamp': '1409735669', 'nonce': '1320562132',
                                               'signature': '16120ec1b8dbb870f510d87ce6bc2463eae6ca2b', 'echostr': 'connected'})

        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.text, '{"error": "服务器内部错误", "code": 10000002}')

    def test_lack_keys(self):
        r = requests.get(url=self.url, params={
                         'nonce': '1320562132', 'signature': '4dbdbe7c66c7d80b6b2b59e138a58484f915256b', 'echostr': 'connected'})
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.text, '{"error": "参数不正确", "code": 10000001}')


if __name__ == '__main__':
    unittest.main()
