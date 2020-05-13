from unittest import TestCase
import requests
from app.view.conversation_manager import generate_token
import json


class SearchStatementTestCase(TestCase):
    """
    Unit tests for the Admin Search Statement.
    LJF: all tests clear 2020-5-13
    """

    def setUp(self):
        self.myheaders = {'Content-Type': 'application/json'}
        self.token = generate_token(b'buaa', 3600)
        # super().setUp()

    def test_no_attribute(self):
        r = requests.get(
            'http://localhost:5000/admin/search_statement',
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "参数不正确", "code": 10000001}')
        self.assertEqual(r.status_code, 400)

    def test_no_username(self):
        r = requests.get(
            'http://localhost:5000/admin/search_statement?token=111&id=',
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "参数不正确", "code": 10000001}')
        self.assertEqual(r.status_code, 400)

    def test_no_token(self):
        r = requests.get(
            'http://localhost:5000/admin/search_statement?username=wechatterbot&id=1',
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "参数不正确", "code": 10000001}')
        self.assertEqual(r.status_code, 400)

    def test_wrong_username(self):
        r = requests.get(
            'http://localhost:5000/admin/search_statement?username=wechatterwhat' +
            '&token='+self.token+'&id=1',
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "Token验证失败", "code": 10000044}')
        self.assertEqual(r.status_code, 401)

    def test_wrong_token(self):
        wrong_token = generate_token(b'what', 3600)
        r = requests.get(
            'http://localhost:5000/admin/search_statement?username=wechatterbot' +
            '&token=' + wrong_token + '&id=1',
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "Token验证失败", "code": 10000044}')
        self.assertEqual(r.status_code, 401)

    def test_empty_id_and_empty_text(self):
        r = requests.get(
            'http://localhost:5000/admin/search_statement?username=wechatterbot' +
            '&token=' + self.token + '&id=&text=',
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "参数不正确", "code": 10000001}')
        self.assertEqual(r.status_code, 400)

    def test_empty_id_and_no_text(self):
        r = requests.get(
            'http://localhost:5000/admin/search_statement?username=wechatterbot' +
            '&token=' + self.token + '&id=',
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "参数不正确", "code": 10000001}')
        self.assertEqual(r.status_code, 400)

    def test_no_id_and_empty_text(self):
        r = requests.get(
            'http://localhost:5000/admin/search_statement?username=wechatterbot' +
            '&token=' + self.token + '&text=',
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "参数不正确", "code": 10000001}')
        self.assertEqual(r.status_code, 400)

    def test_no_id_and_no_text(self):
        r = requests.get(
            'http://localhost:5000/admin/search_statement?username=wechatterbot' +
            '&token=' + self.token,
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "参数不正确", "code": 10000001}')
        self.assertEqual(r.status_code, 400)

    def test_id_not_a_number(self):
        r = requests.get(
            'http://localhost:5000/admin/search_statement?username=wechatterbot' +
            '&token=' + self.token+'&id=string',
            headers=self.myheaders
        )
        self.assertEqual(r.text, '{"error": "参数不正确", "code": 10000001}')

    def test_successful_search_with_id(self):
        r = requests.get(
            'http://localhost:5000/admin/search_statement?username=wechatterbot' +
            '&token=' + self.token + '&id=1',
            headers=self.myheaders
        )
        result = json.loads(r.text)
        statements = result['statements']
        self.assertEqual(statements[0]['id'], 1)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['number'], 1)

    def test_successful_search_with_text(self):
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
            'http://localhost:5000/admin/search_statement?username=wechatterbot' +
            '&token=' + self.token + '&text=临时对话内容',
            headers=self.myheaders
        )
        result = json.loads(r.text)
        statements = result['statements']
        requests.get(
            'http://localhost:5000/admin/delete_statement?username=wechatterbot' +
            '&token=' + self.token + '&sid=' + str(s_id),
            headers=self.myheaders
        )
        self.assertEqual(statements[0]['text'], u"临时对话内容")
        self.assertEqual(r.status_code, 200)
