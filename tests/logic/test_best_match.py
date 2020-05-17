from app.chatterbot.logic import BestMatch
from app.chatterbot.conversation import Statement
from tests.base_case import ChatBotTestCase
from app.chatterbot.storage import storage_adapter_new


class BestMatchTestCase(ChatBotTestCase):
    """
    Unit tests for the BestMatch logic adapter.
    """

    def setUp(self):
        super().setUp()
        self.adapter = BestMatch(self.chatbot)

    def test_no_data(self):
        """
        If there is no data to return, an exception should be raised.
        """
        statement = Statement(text='你想干什么')
        self.assertRaises(storage_adapter_new.StorageAdapterNew.EmptyDatabaseException, self.adapter.process, statement)

    def test_no_choices(self):
        """
        The input should be returned as the closest match if there
        are no other results to return.
        """
        self.chatbot.storage.create(text='罗马')

        statement = Statement(text='你的问题是什么')
        response = self.adapter.process(statement)

        self.assertEqual(response.text, '罗马')
        self.assertEqual(response.confidence, 0)

    def test_no_known_responses(self):
        """
        A match can be selected which has no known responses.
        In this case a random response will be returned, but the confidence
        should be zero because it is a random choice.
        """
        from unittest.mock import MagicMock

        self.chatbot.storage.update = MagicMock()
        self.chatbot.storage.count = MagicMock(return_value=1)
        self.chatbot.storage.get_random = MagicMock(
            return_value=Statement(text='罗马')
        )

        match = self.adapter.process(Statement(text='巴拉巴拉'))

        self.assertEqual(match.confidence, 0)
        self.assertEqual(match.text, '罗马')

    def test_match_with_no_response(self):
        """
        A response to the input should be returned if a response is known.
        """
        self.chatbot.storage.create(
            text='去吃披萨',
            in_response_to='你想干什么'
        )

        statement = Statement(text='你想干什么')
        response = self.adapter.process(statement)

        self.assertEqual(response.text, '去吃披萨')
        self.assertEqual(response.confidence, 0)

    def test_match_with_response(self):
        """
        The response to the input should be returned if a response is known.
        """
        self.chatbot.storage.create(
            text='去吃披萨',
            in_response_to='你想干什么'
        )
        self.chatbot.storage.create(
            text='你想干什么'
        )

        statement = Statement(text='你想干什么')
        response = self.adapter.process(statement)

        self.assertEqual(response.text, '去吃披萨')
        self.assertEqual(response.confidence, 1)

    def test_excluded_words(self):
        """
        Test that the logic adapter cannot return a response containing
        any of the listed words for exclusion.
        """
        self.chatbot.storage.create(
            text='我喜欢音乐'
        )
        self.chatbot.storage.create(
            text='音乐很无聊',
            in_response_to='我喜欢音乐'
        )
        self.chatbot.storage.create(
            text='音乐很有趣',
            in_response_to='我喜欢音乐'
        )

        self.adapter.excluded_words = ['无聊']

        response = self.adapter.process(Statement(text='我喜欢音乐'))

        self.assertEqual(response.confidence, 1)
        self.assertEqual(response.text, '音乐很有趣')

    def test_low_confidence_options_list(self):
        """
        Test the case that a high confidence response is not known.
        """
        self.adapter.default_responses = [
            Statement(text='没有')
        ]

        statement = Statement(text='那里有土豆么')
        match = self.adapter.process(statement)

        self.assertEqual(match.confidence, 0)
        self.assertEqual(match.text, '没有')
