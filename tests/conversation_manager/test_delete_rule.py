from unittest import TestCase
from app import create_app
from app.view.conversation_manager import generate_token
import json


class DeleteRuleTestCase(TestCase):
    """
    Unit tests for the Admin Delete Rule.
    LJF: all tests clear 2020-5-13
    """

    def setUp(self):
        self.app = create_app().test_client()
        self.myheaders = {'Content-Type': 'application/json'}
        self.token = generate_token(b'buaa', 3600)
        # super().setUp()

    def test_no_attribute(self):
        r = self.app.get(
            'admin/delete_rule',
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000001)
        self.assertEqual(r.status_code, 400)

    def test_no_username(self):
        r = self.app.get(
            'admin/delete_rule?token=111&rid=1',
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000001)
        self.assertEqual(r.status_code, 400)

    def test_no_token(self):
        r = self.app.get(
            'admin/delete_rule?username=wechatterbot&rid=1',
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000001)
        self.assertEqual(r.status_code, 400)

    def test_wrong_username(self):
        r = self.app.get(
            'admin/delete_rule?username=wechatterwhat' +
            '&token='+self.token+'&rid=1',
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000044)
        self.assertEqual(r.status_code, 401)

    def test_wrong_token(self):
        wrong_token = generate_token(b'what', 3600)
        r = self.app.get(
            'admin/delete_rule?username=wechatterbot' +
            '&token=' + wrong_token + '&rid=1',
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000044)
        self.assertEqual(r.status_code, 401)

    def test_no_id(self):
        r = self.app.get(
            'admin/delete_rule?username=wechatterbot' +
            '&token=' + self.token,
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000046)

    def test_empty_id(self):
        r = self.app.get(
            'admin/delete_rule?username=wechatterbot' +
            '&token=' + self.token + '&rid=',
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000046)
        self.assertEqual(r.status_code, 400)

    def test_id_not_a_number(self):
        r = self.app.get(
            'admin/delete_rule?username=wechatterbot' +
            '&token=' + self.token + '&rid=string',
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
            'admin/create_rule',
            data=json.dumps(data),
            headers=self.myheaders
        )
        result = json.loads(r1.data.decode('utf-8'))
        rule = result['rule']
        r_id = rule['id']

        r = self.app.get(
            'admin/delete_rule?username=wechatterbot' +
            '&token=' + self.token + '&rid=' + str(r_id),
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['code'], 1)
