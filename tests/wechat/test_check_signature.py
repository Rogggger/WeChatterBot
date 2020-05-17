import unittest
from unittest import TestCase
from app import create_app


class CheckSignatureTestCase(TestCase):
    def setUp(self):
        self.app = create_app().test_client()
        self.pre = '/wx/'

    def test_valid_signature(self):
        r = self.app.get(self.pre,
                         query_string={
                             'timestamp': '1409735669',
                             'nonce': '1320562132',
                             'signature':
                             '4dbdbe7c66c7d80b6b2b59e138a58484f915256b',
                             'echostr': 'connected'
                         })
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data, b'connected')

    def test_invalid_signature(self):
        r = self.app.get(self.pre,
                         query_string={
                             'timestamp': '1409735669',
                             'nonce': '1320562132',
                             'signature':
                             '16120ec1b8dbb870f510d87ce6bc2463eae6ca2b',
                             'echostr': 'connected'
                         })

        self.assertEqual(r.status_code, 400)
        ret = r.data.decode('utf-8')
        self.assertEqual(ret,'{"code": 10000002, "error": "服务器内部错误"}')
        #self.assertEqual(ret, '{"error": "服务器内部错误", "code": 10000002}')

    def test_lack_keys(self):
        r = self.app.get(self.pre,
                         query_string={
                             'nonce': '1320562132',
                             'signature':
                             '4dbdbe7c66c7d80b6b2b59e138a58484f915256b',
                             'echostr': 'connected'
                         })
        self.assertEqual(r.status_code, 400)
        ret = r.data.decode('utf-8')
        self.assertEqual(ret, '{"code": 10000001, "error": "参数不正确"}')

if __name__ == '__main__':
    unittest.main()
