from unittest import TestCase
import requests
from app.view.conversation_manager import generate_token
import json


class CreateStatementTestCase(TestCase):
    """
    Unit tests for the Create Statement method.
    LJF: all tests clear 2020-5-12
    """

    def setUp(self):
        self.myheaders = {'Content-Type': 'application/json'}
        self.token = generate_token(b'buaa', 3600)
        # super().setUp()

    def test_no_attribute(self):
        data = {}
        r = requests.post(
            'http://localhost:5000/admin/create_statement',
            json.dumps(data),
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "参数不正确", "code": 10000001}')
        self.assertEqual(r.status_code, 400)

    def test_no_text(self):
        data = {
            'response': '对话回复',
            'username': 'wechatterbot',
            'token': self.token
        }
        r = requests.post(
            'http://localhost:5000/admin/create_statement',
            json.dumps(data),
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "参数不正确", "code": 10000001}')
        self.assertEqual(r.status_code, 400)

    def test_no_response(self):
        data = {
            'text': '对话内容',
            'username': 'wechatterbot',
            'token': self.token
        }
        r = requests.post(
            'http://localhost:5000/admin/create_statement',
            json.dumps(data),
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "参数不正确", "code": 10000001}')
        self.assertEqual(r.status_code, 400)

    def test_no_username(self):
        data = {
            'response': '对话回复',
            'token': self.token,
            'text': '对话内容'
        }
        r = requests.post(
            'http://localhost:5000/admin/create_statement',
            json.dumps(data),
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "参数不正确", "code": 10000001}')
        self.assertEqual(r.status_code, 400)

    def test_wrong_json(self):
        data = {
            'response': '对话回复',
            'text': '对话内容',
            'username': 'wechatterbot',
            'token': self.token
        }
        r = requests.post(
            'http://localhost:5000/admin/create_statement',
            data,
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "Json格式错误", "code": 10000041}')
        self.assertEqual(r.status_code, 400)

    def test_token_check_fail(self):
        data = {
            'response': '对话回复',
            'text': '对话内容',
            'username': 'wechatterwhat',
            'token': self.token
        }
        r = requests.post(
            'http://localhost:5000/admin/create_statement',
            json.dumps(data),
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "Token验证失败", "code": 10000044}')
        self.assertEqual(r.status_code, 401)

    def test_empty_text(self):
        data = {
            'response': '对话回复',
            'text': '',
            'username': 'wechatterbot',
            'token': self.token
        }
        r = requests.post(
            'http://localhost:5000/admin/create_statement',
            json.dumps(data),
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "text或response为空", "code": 10000045}')
        self.assertEqual(r.status_code, 400)

    def test_empty_response(self):
        data = {
            'response': '',
            'text': '对话内容',
            'username': 'wechatterbot',
            'token': self.token
        }
        r = requests.post(
            'http://localhost:5000/admin/create_statement',
            json.dumps(data),
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "text或response为空", "code": 10000045}')
        self.assertEqual(r.status_code, 400)

    def test_successful_creation(self):
        data = {
            'response': '对话回复',
            'text': '对话内容',
            'username': 'wechatterbot',
            'token': self.token
        }
        r = requests.post(
            'http://localhost:5000/admin/create_statement',
            json.dumps(data),
            headers=self.myheaders
        )
        result = json.loads(r.text)
        statement = result['statement']
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['code'], 1)
        self.assertEqual(statement['text'], "对话内容")

    def test_successful_with_tags(self):
        data = {
            'response': '对话回复',
            'text': '对话内容',
            'username': 'wechatterbot',
            'token': self.token,
            'tags': 'test'
        }
        r = requests.post(
            'http://localhost:5000/admin/create_statement',
            json.dumps(data),
            headers=self.myheaders
        )
        result = json.loads(r.text)
        statement = result['statement']
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['code'], 1)
        self.assertEqual(statement['text'], "对话内容")
