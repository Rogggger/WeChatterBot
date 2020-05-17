from unittest import TestCase
from app import create_app
from app.view.conversation_manager import generate_token
import json


class DeleteStatementTestCase(TestCase):
    """
    Unit tests for the Admin Delete Statement.
    LJF: all tests clear 2020-5-13
    """

    def setUp(self):
        self.app = create_app().test_client()
        self.myheaders = {'Content-Type': 'application/json'}
        self.token = generate_token(b'buaa', 3600)
        # super().setUp()

    def test_no_attribute(self):
        r = self.app.get(
            'admin/delete_statement',
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000001)
        self.assertEqual(r.status_code, 400)

    def test_no_username(self):
        r = self.app.get(
            'admin/delete_statement?token=111&sid=1',
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000001)
        self.assertEqual(r.status_code, 400)

    def test_no_token(self):
        r = self.app.get(
            'admin/delete_statement?username=wechatterbot&sid=1',
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000001)
        self.assertEqual(r.status_code, 400)

    def test_wrong_username(self):
        r = self.app.get(
            'admin/delete_statement?username=wechatterwhat' +
            '&token=' + self.token + '&sid=1',
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000044)
        self.assertEqual(r.status_code, 401)

    def test_wrong_token(self):
        wrong_token = generate_token(b'what', 3600)
        r = self.app.get(
            'admin/delete_statement?username=wechatterbot' +
            '&token=' + wrong_token + '&sid=1',
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000044)
        self.assertEqual(r.status_code, 401)

    def test_no_id(self):
        r = self.app.get(
            'admin/delete_statement?username=wechatterbot' +
            '&token=' + self.token,
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000046)

    def test_empty_id(self):
        r = self.app.get(
            'admin/delete_statement?username=wechatterbot' +
            '&token=' + self.token + '&sid=',
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000046)
        self.assertEqual(r.status_code, 400)

    def test_id_not_a_number(self):
        r = self.app.get(
            'admin/delete_statement?username=wechatterbot' +
            '&token=' + self.token + '&sid=string',
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000001)
        self.assertEqual(r.status_code, 400)

    def test_successful_delete(self):
        data = {
            'response': '回复规则',
            'text': '规则内容',
            'username': 'wechatterbot',
            'token': self.token
        }
        r1 = self.app.post(
            'admin/create_statement',
            data=json.dumps(data),
            headers=self.myheaders
        )
        result = json.loads(r1.data.decode('utf-8'))
        statement = result['statement']
        s_id = statement['id']

        r = self.app.get(
            'admin/delete_statement?username=wechatterbot' +
            '&token=' + self.token + '&sid=' + str(s_id),
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['code'], 1)
        
