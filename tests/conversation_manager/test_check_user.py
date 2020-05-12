from unittest import TestCase
import requests
from app.libs.chatbot import chatbot


class CertifyUserTestCase(TestCase):
    """
    Unit tests for the Certify User method.
    LJF: not all tests clear
    """
    def setUp(self):
        self.chatbot = chatbot
        self.myheaders = {'Content-Type': 'application/json'}
        # super().setUp()

    def test_no_attribute(self):
        r = requests.get(
            'http://localhost:5000/admin/certify',
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "参数不正确", "code": 10000001}')
        self.assertEqual(r.status_code, 400)

    def test_no_username(self):
        r = requests.get(
            'http://localhost:5000/admin/login?password=111',
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "参数不正确", "code": 10000001}')
        self.assertEqual(r.status_code, 400)

    def test_no_password(self):
        r = requests.get(
            'http://localhost:5000/admin/login?username=111',
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "参数不正确", "code": 10000001}')
        self.assertEqual(r.status_code, 400)

    def test_wrong_username(self):
        r = requests.get(
            'http://localhost:5000/admin/login?username=111&password=bbb',
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "账户不存在", "code": 10000012}')
        self.assertEqual(r.status_code, 400)

    def test_wrong_password(self):
        r = requests.get(
            'http://localhost:5000/admin/login?username=wechatterbot&password=bbb',
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "密码不正确", "code": 10000013}')
        self.assertEqual(r.status_code, 400)

    def test_successful_login(self):
        r = requests.get(
            'http://localhost:5000/admin/login?username=wechatterbot&password=buaawechatterbot',
            headers=self.myheaders
        )
        print(r.text)
        self.assertEqual(r.status_code, 200)
