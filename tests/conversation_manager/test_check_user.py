from unittest import TestCase
from app.view.conversation_manager import generate_token
import json
from app import create_app


class CheckUserTestCase(TestCase):
    """
    Unit tests for the Certify User method.
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
            'admin/certify',
            data=json.dumps(data),
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000001)
        self.assertEqual(r.status_code, 400)

    def test_no_username(self):
        data = {
            'token': 'wrong_token'
        }
        r = self.app.post(
            'admin/certify',
            data=json.dumps(data),
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000001)
        self.assertEqual(r.status_code, 400)

    def test_no_token(self):
        data = {
            'username': 'wechatterbot'
        }
        r = self.app.post(
            'admin/certify',
            data=json.dumps(data),
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000001)
        self.assertEqual(r.status_code, 400)

    def test_wrong_username(self):
        data = {
            'username': 'wechatterwhat',
            'token': self.token
        }
        r = self.app.post(
            'admin/certify',
            data=json.dumps(data),
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000044)
        self.assertEqual(r.status_code, 401)

    def test_wrong_json(self):
        data = {
            'username': 'wechatterbot',
            'token': self.token
        }
        r = self.app.post(
            'admin/certify',
            data=data,
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000041)
        self.assertEqual(r.status_code, 400)

    def test_check_fail(self):
        wrong_token = generate_token(b'what', 3600)
        data = {
            'username': 'wechatterbot',
            'token': wrong_token
        }
        r = self.app.post(
            'admin/certify',
            data=json.dumps(data),
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000044)
        self.assertEqual(r.status_code, 401)

    def test_check_success(self):
        data = {
            'username': 'wechatterbot',
            'token': self.token
        }
        r = self.app.post(
            'admin/certify',
            data=json.dumps(data),
            headers=self.myheaders
        )
        self.assertEqual(r.status_code, 200)
