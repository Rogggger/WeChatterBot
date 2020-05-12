from unittest import TestCase
import requests
from app.view.conversation_manager import generate_token
import json


class DeleteRuleTestCase(TestCase):
    """
    Unit tests for the Admin Delete Rule.
    LJF: all tests clear 2020-5-13
    """

    def setUp(self):
        self.myheaders = {'Content-Type': 'application/json'}
        self.token = generate_token(b'buaa', 3600)
        # super().setUp()

    def test_no_attribute(self):
        r = requests.get(
            'http://localhost:5000/admin/delete_rule',
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "参数不正确", "code": 10000001}')
        self.assertEqual(r.status_code, 400)

    def test_no_username(self):
        r = requests.get(
            'http://localhost:5000/admin/delete_rule?token=111&rid=1',
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "参数不正确", "code": 10000001}')
        self.assertEqual(r.status_code, 400)

    def test_no_token(self):
        r = requests.get(
            'http://localhost:5000/admin/delete_rule?username=wechatterbot&rid=1',
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "参数不正确", "code": 10000001}')
        self.assertEqual(r.status_code, 400)

    def test_wrong_username(self):
        r = requests.get(
            'http://localhost:5000/admin/delete_rule?username=wechatterwhat' +
            '&token='+self.token+'&rid=1',
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "Token验证失败", "code": 10000044}')
        self.assertEqual(r.status_code, 401)

    def test_wrong_token(self):
        wrong_token = generate_token(b'what', 3600)
        r = requests.get(
            'http://localhost:5000/admin/delete_rule?username=wechatterbot' +
            '&rid=1' + '&token=' + wrong_token,
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "Token验证失败", "code": 10000044}')
        self.assertEqual(r.status_code, 401)

    def test_no_id(self):
        r = requests.get(
            'http://localhost:5000/admin/delete_rule?username=wechatterbot' +
            '&token=' + self.token,
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "参数不正确", "code": 10000001}')

    def test_empty_id(self):
        r = requests.get(
            'http://localhost:5000/admin/delete_rule?username=wechatterbot' +
            '&token=' + self.token + '&rid=',
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "参数不正确", "code": 10000001}')
        self.assertEqual(r.status_code, 400)

    def test_successful_delete(self):
        data = {
            'response': '临时回复规则',
            'text': '临时规则内容',
            'username': 'wechatterbot',
            'token': self.token
        }
        r1 = requests.post(
            'http://localhost:5000/admin/create_rule',
            json.dumps(data),
            headers=self.myheaders
        )
        result = json.loads(r1.text)
        rule = result['rule']
        r_id = rule['id']

        r = requests.get(
            'http://localhost:5000/admin/delete_rule?username=wechatterbot' +
            '&token=' + self.token + '&rid='+str(r_id),
            headers=self.myheaders
        )
        result = json.loads(r.text)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['code'], 1)
