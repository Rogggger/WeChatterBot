from unittest import TestCase
from app.view.conversation_manager import generate_token
import json
from app import create_app


class CreateRuleTestCase(TestCase):
    """
    Unit tests for the Create Rule method.
    LJF: all tests clear 2020-5-12
    """

    def setUp(self):
        self.myheaders = {'Content-Type': 'application/json'}
        self.token = generate_token(b'buaa', 3600)
        self.app = create_app().test_client()
        # super().setUp()

    def test_no_attribute(self):
        data = {}
        r = self.app.post(
            'admin/create_rule',
            data=json.dumps(data),
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000001)
        self.assertEqual(r.status_code, 400)

    def test_no_text(self):
        data = {
            'response': '回复规则',
            'username': 'wechatterbot',
            'token': self.token
        }
        r = self.app.post(
            'admin/create_rule',
            data=json.dumps(data),
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000001)
        self.assertEqual(r.status_code, 400)

    def test_no_response(self):
        data = {
            'text': '规则内容',
            'username': 'wechatterbot',
            'token': self.token
        }
        r = self.app.post(
            'admin/create_rule',
            data=json.dumps(data),
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000001)
        self.assertEqual(r.status_code, 400)

    def test_no_username(self):
        data = {
            'response': '回复规则',
            'token': self.token,
            'text': '对话内容'
        }
        r = self.app.post(
            'admin/create_rule',
            data=json.dumps(data),
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000001)
        self.assertEqual(r.status_code, 400)

    def test_wrong_json(self):
        data = {
            'response': '回复规则',
            'text': '规则内容',
            'username': 'wechatterbot',
            'token': self.token
        }
        r = self.app.post(
            'admin/create_rule',
            data=data,
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000041)
        self.assertEqual(r.status_code, 400)

    def test_token_check_fail(self):
        data = {
            'response': '回复规则',
            'text': '规则内容',
            'username': 'wechatterwhat',
            'token': self.token
        }
        r = self.app.post(
            'admin/create_rule',
            data=json.dumps(data),
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000044)
        self.assertEqual(r.status_code, 401)

    def test_empty_text(self):
        data = {
            'response': '回复规则',
            'text': '',
            'username': 'wechatterbot',
            'token': self.token
        }
        r = self.app.post(
            'admin/create_rule',
            data=json.dumps(data),
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000045)
        self.assertEqual(r.status_code, 400)

    def test_empty_response(self):
        data = {
            'response': '',
            'text': '规则内容',
            'username': 'wechatterbot',
            'token': self.token
        }
        r = self.app.post(
            'admin/create_rule',
            data=json.dumps(data),
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000045)
        self.assertEqual(r.status_code, 400)

    def test_successful_creation(self):
        data = {
            'response': '回复规则',
            'text': '规则内容',
            'username': 'wechatterbot',
            'token': self.token
        }
        r = self.app.post(
            'admin/create_rule',
            data=json.dumps(data),
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        rule = result['rule']
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['code'], 1)
        self.assertEqual(rule['text'], "规则内容")
