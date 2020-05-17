from unittest import TestCase
from app import create_app
import json


class LoginTestCase(TestCase):
    """
    Unit tests for the Admin Login.
    LJF: all tests clear 2020-5-12
    """

    def setUp(self):
        self.app = create_app().test_client()
        self.myheaders = {'Content-Type': 'application/json'}
        # super().setUp()

    def test_no_attribute(self):
        r = self.app.get(
            'http://localhost:5000/admin/login',
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000001)
        self.assertEqual(r.status_code, 400)

    def test_no_username(self):
        r = self.app.get(
            'http://localhost:5000/admin/login?password=111',
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000001)
        self.assertEqual(r.status_code, 400)

    def test_no_password(self):
        r = self.app.get(
            'http://localhost:5000/admin/login?username=wechatterwhat',
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000001)
        self.assertEqual(r.status_code, 400)

    def test_wrong_username(self):
        r = self.app.get(
            'http://localhost:5000/admin/login?username=wechatterwhat&password=bbb',
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000012)
        self.assertEqual(r.status_code, 400)

    def test_wrong_password(self):
        r = self.app.get(
            'http://localhost:5000/admin/login?username=wechatterbot&password=bbb',
            headers=self.myheaders
        )
        result = json.loads(r.data.decode('utf-8'))
        self.assertEqual(result['code'], 10000013)
        self.assertEqual(r.status_code, 400)

    def test_successful_login(self):
        r = self.app.get(
            'http://localhost:5000/admin/login?username=wechatterbot&password=buaawechatterbot',
            headers=self.myheaders
        )
        self.assertEqual(r.status_code, 200)
