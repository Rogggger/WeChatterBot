from tests.base_case import ChatBotTestCase
from app.chatterbot.logic import ConstAdapter
from app.chatterbot.conversation import Statement


class SpecificResponseAdapterTestCase(ChatBotTestCase):
    """
    Test cases for the SpecificResponseAdapter
    """

    def setUp(self):
        super().setUp()
        self.adapter = ConstAdapter(self.chatbot,const_response='看不懂唉',const_confidence=0.1)

    def test_true(self):
        """
        Test the case that an exact match is given.
        """
        statement = Statement(text='你想干什么')
        match = self.adapter.process(statement)

        self.assertEqual(match.confidence, 0.1)
        self.assertEqual(match, self.adapter.response_statement)

