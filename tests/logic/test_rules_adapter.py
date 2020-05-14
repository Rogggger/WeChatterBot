from tests.base_case import ChatBotTestCase
from app.chatterbot.logic import RulesResponseAdapter
from app.chatterbot.conversation import Statement


class SpecificResponseAdapterTestCase(ChatBotTestCase):
    """
    Test cases for the SpecificResponseAdapter
    """

    def setUp(self):
        super().setUp()
        self.adapter = RulesResponseAdapter(self.chatbot)

    def test_exact_match(self):
        """
        Test the case that an exact match is given.
        """
        self.chatbot.storage.create_rule(text='你喜欢音乐么',in_response_to='喜欢')
        statement = Statement(text='你喜欢音乐么')
        match = self.adapter.process(statement)

        self.assertEqual(match.confidence, 10)
        self.assertEqual(match.text,'喜欢')

    def test_not_exact_match(self):
        """
        Test the case that an exact match is not given.
        """
        self.chatbot.storage.create_rule(text='你喜欢音乐么',in_response_to='喜欢')
        statement = Statement(text='你要干什么')
        match = self.adapter.process(statement)

        self.assertEqual(match.confidence, 0)
        self.assertEqual(match.text,'')
