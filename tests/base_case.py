from unittest import TestCase
from app.chatterbot_api.chatterbot import ChatBot
from typing import Sized

Keyword_args = {
    # Run the test database in-memory
    'database_uri': None,
    # Don't execute initialization processes such as downloading required data
    'initialize': False
}
class ChatBotTestCase(TestCase):
    """
    base test case for chatbot
    """
    @property
    def kwargs(self):
        return Keyword_args

    def setUp(self):
        self.chatbot = ChatBot('Test Bot', **self.kwargs)

    def tearDown(self):
        """
        Remove the test database.
        """
        self.chatbot.storage.drop()

    def assertIsLength(self, item, length):
        """
        Assert that an iterable has the given length.

        :param item: an iterable item
        :type item: Sized
        :param length: asserted length of item
        :type length: int
        """
        if len(item) != length:
            raise AssertionError(f'Length {len(item)} is not equal to {length}')


class ChatBotMongoTestCase(ChatBotTestCase):

    @classmethod
    def setUpClass(cls):
        from pymongo.errors import ServerSelectionTimeoutError
        from pymongo import MongoClient

        # Skip these tests if a mongo client is not running
        try:
            client = MongoClient(
                serverSelectionTimeoutMS=0.1
            )
            client.server_info()

        except ServerSelectionTimeoutError:
            raise SkipTest('Unable to connect to Mongo DB.')

    def get_kwargs(self):
        kwargs = super().kwargs
        kwargs['database_uri'] = 'mongodb://localhost:27017/chatterbot_test_database'
        kwargs['storage_adapter'] = 'chatterbot.storage.MongoDatabaseAdapter'
        return kwargs


class ChatBotSQLTestCase(ChatBotTestCase):

    def get_kwargs(self):
        kwargs = super().kwargs
        kwargs['storage_adapter'] = 'chatterbot.storage.SQLStorageAdapter'
        return kwargs