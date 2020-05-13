from unittest import TestCase
import requests
from app.view.conversation_manager import generate_token
import json


class CheckUserTestCase(TestCase):
    """
    Unit tests for the Certify User method.
    LJF: all tests clear 2020-5-12
    """

    def setUp(self):
        self.myheaders = {'Content-Type': 'application/json'}
        self.token = generate_token(b'buaa', 3600)
        # super().setUp()

    def test_no_attribute(self):
        data = {}
        r = requests.post(
            'http://localhost:5000/admin/certify',
            json.dumps(data),
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "参数不正确", "code": 10000001}')
        self.assertEqual(r.status_code, 400)

    def test_no_username(self):
        data = {
            'token': 'wrong_token'
        }
        r = requests.post(
            'http://localhost:5000/admin/certify',
            json.dumps(data),
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "参数不正确", "code": 10000001}')
        self.assertEqual(r.status_code, 400)

    def test_no_token(self):
        data = {
            'username': 'wechatterbot'
        }
        r = requests.post(
            'http://localhost:5000/admin/certify',
            json.dumps(data),
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "参数不正确", "code": 10000001}')
        self.assertEqual(r.status_code, 400)

    def test_wrong_username(self):
        data = {
            'username': 'wechatterwhat',
            'token': self.token
        }
        r = requests.post(
            'http://localhost:5000/admin/certify',
            json.dumps(data),
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "Token验证失败", "code": 10000044}')
        self.assertEqual(r.status_code, 401)

    def test_wrong_json(self):
        data = {
            'username': 'wechatterbot',
            'token': self.token
        }
        r = requests.post(
            'http://localhost:5000/admin/certify',
            data,
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "Json格式错误", "code": 10000041}')
        self.assertEqual(r.status_code, 400)

    def test_check_fail(self):
        wrong_token = generate_token(b'what', 3600)
        data = {
            'username': 'wechatterbot',
            'token': wrong_token
        }
        r = requests.post(
            'http://localhost:5000/admin/certify',
            json.dumps(data),
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "Token验证失败", "code": 10000044}')
        self.assertEqual(r.status_code, 401)

    def test_check_success(self):
        data = {
            'username': 'wechatterbot',
            'token': self.token
        }
        r = requests.post(
            'http://localhost:5000/admin/certify',
            json.dumps(data),
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"code": 1}')
        self.assertEqual(r.status_code, 200)
