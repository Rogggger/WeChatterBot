from unittest import TestCase
import requests
from app.view.conversation_manager import generate_token
import json


class DeleteStatementTestCase(TestCase):
    """
    Unit tests for the Admin Delete Statement.
    LJF: all tests clear 2020-5-13
    """
    def setUp(self):
        self.myheaders = {'Content-Type': 'application/json'}
        self.token = generate_token(b'buaa', 3600)
        # super().setUp()

    def test_no_attribute(self):
        r = requests.get(
            'http://localhost:5000/admin/delete_statement',
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "参数不正确", "code": 10000001}')
        self.assertEqual(r.status_code, 400)

    def test_no_username(self):
        r = requests.get(
            'http://localhost:5000/admin/delete_statement?token=111&sid=1',
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "参数不正确", "code": 10000001}')
        self.assertEqual(r.status_code, 400)

    def test_no_token(self):
        r = requests.get(
            'http://localhost:5000/admin/delete_statement?username=wechatterbot&sid=1',
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "参数不正确", "code": 10000001}')
        self.assertEqual(r.status_code, 400)

    def test_wrong_username(self):
        r = requests.get(
            'http://localhost:5000/admin/delete_statement?username=wechatterwhat' +
            '&token='+self.token+'&sid=1',
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "Token验证失败", "code": 10000044}')
        self.assertEqual(r.status_code, 401)

    def test_wrong_token(self):
        wrong_token = generate_token(b'what', 3600)
        r = requests.get(
            'http://localhost:5000/admin/delete_statement?username=wechatterbot' +
            '&sid=1' + '&token=' + wrong_token,
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "Token验证失败", "code": 10000044}')
        self.assertEqual(r.status_code, 401)

    def test_no_id(self):
        r = requests.get(
            'http://localhost:5000/admin/delete_statement?username=wechatterbot' +
            '&token=' + self.token,
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "参数不正确", "code": 10000001}')

    def test_empty_id(self):
        r = requests.get(
            'http://localhost:5000/admin/delete_statement?username=wechatterbot' +
            '&token=' + self.token + '&sid=',
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "参数不正确", "code": 10000001}')
        self.assertEqual(r.status_code, 400)

    def test_successful_delete(self):
        data = {
            'response': '临时对话回复',
            'text': '临时对话内容',
            'username': 'wechatterbot',
            'token': self.token
        }
        r1 = requests.post(
            'http://localhost:5000/admin/create_statement',
            json.dumps(data),
            headers=self.myheaders
        )
        result = json.loads(r1.text)
        statement = result['statement']
        s_id = statement['id']

        r = requests.get(
            'http://localhost:5000/admin/delete_statement?username=wechatterbot' +
            '&token=' + self.token + '&sid='+str(s_id),
            headers=self.myheaders
        )
        result = json.loads(r.text)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['code'], 1)
