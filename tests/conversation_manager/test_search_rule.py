from unittest import TestCase
import requests
from app.view.conversation_manager import generate_token
import json


class SearchRuleTestCase(TestCase):
    """
    Unit tests for the Admin Search Rule.
    LJF: all tests clear 2020-5-13
    """

    def setUp(self):
        self.myheaders = {'Content-Type': 'application/json'}
        self.token = generate_token(b'buaa', 3600)
        # super().setUp()

    def test_no_attribute(self):
        r = requests.get(
            'http://localhost:5000/admin/search_rule',
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "参数不正确", "code": 10000001}')
        self.assertEqual(r.status_code, 400)

    def test_no_username(self):
        r = requests.get(
            'http://localhost:5000/admin/search_rule?token=111&id=',
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "参数不正确", "code": 10000001}')
        self.assertEqual(r.status_code, 400)

    def test_no_token(self):
        r = requests.get(
            'http://localhost:5000/admin/search_rule?username=wechatterbot&id=1',
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "参数不正确", "code": 10000001}')
        self.assertEqual(r.status_code, 400)

    def test_wrong_username(self):
        r = requests.get(
            'http://localhost:5000/admin/search_rule?username=wechatterwhat' +
            '&token='+self.token+'&id=1',
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "Token验证失败", "code": 10000044}')
        self.assertEqual(r.status_code, 401)

    def test_wrong_token(self):
        wrong_token = generate_token(b'what', 3600)
        r = requests.get(
            'http://localhost:5000/admin/search_rule?username=wechatterbot' +
            '&token=' + wrong_token + '&id=1',
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "Token验证失败", "code": 10000044}')
        self.assertEqual(r.status_code, 401)

    def test_empty_id_and_empty_text(self):
        r = requests.get(
            'http://localhost:5000/admin/search_rule?username=wechatterbot' +
            '&token=' + self.token + '&id=&text=',
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "参数不正确", "code": 10000001}')
        self.assertEqual(r.status_code, 400)

    def test_empty_id_and_no_text(self):
        r = requests.get(
            'http://localhost:5000/admin/search_rule?username=wechatterbot' +
            '&token=' + self.token + '&id=',
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "参数不正确", "code": 10000001}')
        self.assertEqual(r.status_code, 400)

    def test_no_id_and_empty_text(self):
        r = requests.get(
            'http://localhost:5000/admin/search_rule?username=wechatterbot' +
            '&token=' + self.token + '&text=',
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "参数不正确", "code": 10000001}')
        self.assertEqual(r.status_code, 400)

    def test_no_id_and_no_text(self):
        r = requests.get(
            'http://localhost:5000/admin/search_rule?username=wechatterbot' +
            '&token=' + self.token,
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "参数不正确", "code": 10000001}')
        self.assertEqual(r.status_code, 400)

    def test_id_not_a_number(self):
        r = requests.get(
            'http://localhost:5000/admin/search_rule?username=wechatterbot' +
            '&token=' + self.token+'&id=string',
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "参数不正确", "code": 10000001}')

    def test_successful_search_with_id(self):
        r = requests.get(
            'http://localhost:5000/admin/search_rule?username=wechatterbot' +
            '&token=' + self.token + '&id=1',
            headers=self.myheaders
        )
        result = json.loads(r.text)
        rules = result['rules']
        self.assertEqual(rules[0]['id'], 1)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['number'], 1)

    def test_successful_search_with_text(self):
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
        statement = result['rule']
        r_id = statement['id']

        r = requests.get(
            'http://localhost:5000/admin/search_rule?username=wechatterbot' +
            '&token=' + self.token + '&text=临时规则内容',
            headers=self.myheaders
        )
        result = json.loads(r.text)
        rules = result['rules']
        self.assertEqual(rules[0]['id'], r_id)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['number'], 1)