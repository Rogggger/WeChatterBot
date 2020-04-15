from unittest import TestCase
import sys
sys.path.append('../app/chatterbot_api')
from chatterbot.conversation import Statement

class StatementTests(TestCase):
    def test_serializer(self):
        statement = Statement(text='A test statement.')
        data = statement.serialize()
        self.assertEqual(statement.text, data['text'])
