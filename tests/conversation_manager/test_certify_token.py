from unittest import TestCase
from app.view.conversation_manager import certify_token, generate_token
import base64
import json


class CertifyTokenTestCase(TestCase):
    """
    Unit tests for the Certify Token method.
    LJF: all tests clear 2020-5-12
    """

    def setUp(self):
        self.myheaders = {'Content-Type': 'application/json'}
        self.token = generate_token(b'buaa', 3600)
        # super().setUp()

    def test_wrong_username(self):
        b, result = certify_token('wechatterwhat', self.token.encode('utf-8'))
        temp = json.loads(result.data.decode('utf-8'))
        self.assertEqual(temp['code'], 10000044)
        self.assertEqual(b, False)

    def test_wrong_struct(self):
        ts_str = 'abc'
        b64_token = base64.b64encode(bytes(ts_str, 'utf-8'), b'-_')
        b, result = certify_token('wechatterbot', b64_token)
        temp = json.loads(result.data.decode('utf-8'))
        self.assertEqual(temp['code'], 10000042)
        self.assertEqual(b, False)

    def test_expired(self):
        expired_token = generate_token(b'buaa', -1)
        b, result = certify_token('wechatterbot', expired_token.encode('utf-8'))
        temp = json.loads(result.data.decode('utf-8'))
        self.assertEqual(temp['code'], 10000043)
        self.assertEqual(b, False)

    def test_wrong_token(self):
        wrong_token = generate_token(b'what', 3600)
        b, result = certify_token('wechatterbot', wrong_token.encode('utf-8'))
        temp = json.loads(result.data.decode('utf-8'))
        self.assertEqual(temp['code'], 10000044)
        self.assertEqual(b, False)

    def test_pass(self):
        b, result = certify_token('wechatterbot', self.token.encode('utf-8'))
        # 不好测token
        self.assertEqual(b, True)
