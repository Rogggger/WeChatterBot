from unittest import TestCase
from app import create_app
from app.view.conversation_manager import generate_token
import json


class UpdateStatementTestCase(TestCase):
    """
    Unit tests for the Update Statement method.
    LJF: all tests clear 2020-5-12
    """

    def setUp(self):
        self.app = create_app().test_client()
        self.myheaders = {'Content-Type': 'application/json'}
        self.token = generate_token(b'buaa', 3600)
        # super().setUp()

    def test_no_attribute(self):
        data = {}
        r = self.app.post(
            'admin/update_statement',
            data=json.dumps(data),
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000001)
        self.assertEqual(r.status_code, 400)

    def test_no_text(self):
        data = {
            'id': 1,
            'response': '对话回复',
            'username': 'wechatterbot',
            'token': self.token
        }
        r = self.app.post(
            'admin/update_statement',
            data=json.dumps(data),
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000001)
        self.assertEqual(r.status_code, 400)

    def test_no_response(self):
        data = {
            'id': 1,
            'text': '对话内容',
            'username': 'wechatterbot',
            'token': self.token
        }
        r = self.app.post(
            'admin/update_statement',
            data=json.dumps(data),
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000001)
        self.assertEqual(r.status_code, 400)

    def test_no_username(self):
        data = {
            'id': 1,
            'response': '对话回复',
            'token': self.token,
            'text': '对话内容'
        }
        r = self.app.post(
            'admin/update_statement',
            data=json.dumps(data),
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000001)
        self.assertEqual(r.status_code, 400)

    def test_no_id(self):
        data = {
            'response': '对话回复',
            'text': '对话内容',
            'username': 'wechatterbot',
            'token': self.token
        }
        r = self.app.post(
            'admin/update_statement',
            data=json.dumps(data),
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000001)
        self.assertEqual(r.status_code, 400)

    def test_wrong_json(self):
        data = {
            'id': 1,
            'response': '对话回复',
            'text': '对话内容',
            'username': 'wechatterbot',
            'token': self.token
        }
        r = self.app.post(
            'admin/update_statement',
            data=data,
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000041)
        self.assertEqual(r.status_code, 400)

    def test_token_check_fail(self):
        data = {
            'id': 1,
            'response': '对话回复',
            'text': '对话内容',
            'username': 'wechatterwhat',
            'token': self.token
        }
        r = self.app.post(
            'admin/update_statement',
            data=json.dumps(data),
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000044)
        self.assertEqual(r.status_code, 401)

    def test_empty_text(self):
        data = {
            'id': 1,
            'response': '对话回复',
            'text': '',
            'username': 'wechatterbot',
            'token': self.token
        }
        r = self.app.post(
            'admin/update_statement',
            data=json.dumps(data),
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000045)
        self.assertEqual(r.status_code, 400)

    def test_empty_response(self):
        data = {
            'id': 1,
            'response': '',
            'text': '对话内容',
            'username': 'wechatterbot',
            'token': self.token
        }
        r = self.app.post(
            'admin/update_statement',
            data=json.dumps(data),
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000045)
        self.assertEqual(r.status_code, 400)

    def test_empty_id(self):
        data = {
            'id': '',
            'response': '回复内容',
            'text': '对话内容',
            'username': 'wechatterbot',
            'token': self.token
        }
        r = self.app.post(
            'admin/update_statement',
            data=json.dumps(data),
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000046)
        self.assertEqual(r.status_code, 400)

    def test_id_not_a_number(self):
        data = {
            'id': 'string',
            'response': '回复内容',
            'text': '对话内容',
            'username': 'wechatterbot',
            'token': self.token
        }
        r = self.app.post(
            'admin/update_statement',
            data=json.dumps(data),
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000001)
        self.assertEqual(r.status_code, 400)

    def test_successful_update(self):
        data = {
            'response': '对话回复',
            'text': '对话内容',
            'username': 'wechatterbot',
            'token': self.token
        }
        r = self.app.post(
            'admin/create_statement',
            data=json.dumps(data),
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        statement = result['statement']
        s_id = statement['id']
        data['id'] = s_id
        data['text'] = '新对话内容'
        r = self.app.post(
            'admin/update_statement',
            data=json.dumps(data),
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        statement = result['statement']
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['code'], 1)
        self.assertEqual(statement['text'], "新对话内容")
