from tests.base_case import ChatBotTestCase
from app.chatterbot.logic import LogicAdapter
from app.chatterbot.conversation import Statement
from app.chatterbot import ChatBot, languages, comparisons, response_selection

kwargs = {
    "logic_adapters": [
        "chatterbot.logic.BestMatch",
        "chatterbot.logic.RulesResponseAdapter",
    ],
    "tagger_language": languages.CHI,
    "statement_comparison_function": comparisons.JaccardSimilarity,
    "response_selection_method": response_selection.get_first_response
}


class ChatterBotResponseTestCase(ChatBotTestCase):

    def setUp(self):
        self.chatbot = ChatBot("Test Bot", **kwargs)
        self.chatbot.storage.create(text='罗马')

    def test_conversation_values_persisted_to_response(self):
        response = self.chatbot.get_response(
            '你好',
            persist_values_to_response={'conversation': 'test 1 你好'}
        )
        self.assertEqual(response.conversation, 'test 1 你好')

    def test_tag_values_persisted_to_response(self):
        response = self.chatbot.get_response(
            '你好',
            persist_values_to_response={'tags': ['你好1', '1你好']}
        )
        self.assertIsLength(response.tags, 2)
        self.assertIn('你好1', response.get_tags())
        self.assertIn('1你好', response.get_tags())

    def test_in_response_to_provided(self):
        """
        Test that the process of looking up the previous response
        in the conversation is ignored if a previous response is provided.
        """
        self.chatbot.get_response(
            text='我很好。',
            in_response_to='你好吗？'
        )
        statement = self.chatbot.storage.filter(
            text='我很好。',
            in_response_to='你好吗？'
        )
        self.assertIsNotNone(statement)

    def test_second_response_unknown(self):
        self.chatbot.storage.create(text='早上好', in_response_to=None)
        self.chatbot.storage.create(text='你好', in_response_to='早上好')

        first_response = self.chatbot.get_response(
            text='早上好',
        )
        second_response = self.chatbot.get_response(
            text='你好么',
        )

        results = list(self.chatbot.storage.filter(text='你好'))
        self.assertAlmostEqual(first_response.confidence,1,1)
        self.assertEqual(first_response.text, '你好')
        self.assertEqual(first_response.in_response_to, '早上好')

        self.assertEqual(second_response.confidence, 0)
        self.assertEqual(second_response.in_response_to, '你好么')

        # Make sure that the second response was saved to the database
        self.assertIsLength(results, 2)
        self.assertEqual(results[0].in_response_to, '早上好')

    def test_get_response_additional_response_selection_parameters(self):
        self.chatbot.storage.create_many([
            Statement('A', conversation='test_1'),
            Statement('B', conversation='test_1', in_response_to='A'),
            Statement('A', conversation='test_2'),
            Statement('C', conversation='test_2', in_response_to='A'),
        ])

        statement = Statement(text='A', conversation='test_3')
        response = self.chatbot.get_response(
            statement,
            additional_response_selection_parameters={'conversation': 'test_2'}
        )

        self.assertEqual(response.text, 'C')
        self.assertEqual(response.conversation, 'test_3')

    def test_special_text(self):
        # Test the case that a unicode string is passed in.
        response = self.chatbot.get_response(u'سلام')
        self.assertGreater(len(response.text), 0)

        # Test the case that the input string contains an emoji.
        response = self.chatbot.get_response(u'👍')
        self.assertGreater(len(response.text), 0)

        # Test the case that a string containing two-byte characters is passed in.
        response = self.chatbot.get_response(u'田中さんにあげて下さい')
        self.assertGreater(len(response.text), 0)

        # Test the case that a string contains "corrupted" text.
        response = self.chatbot.get_response(
            u'Ṱ̺̺̕h̼͓̲̦̳̘̲e͇̣̰̦̬͎ ̢̼̻̱̘h͚͎͙̜̣̲ͅi̦̲̣̰̤v̻͍e̺̭̳̪̰-m̢iͅn̖̺̞̲̯̰d̵̼̟͙̩̼̘̳.̨̹͈̣')
        self.assertGreater(len(response.text), 0)


    def test_get_response_with_text_and_kwargs(self):
        self.chatbot.get_response('你好', conversation='打招呼')

        results = list(self.chatbot.storage.filter(text='你好'))

        self.assertIsLength(results, 1)
        self.assertEqual(results[0].conversation, '打招呼')

    def test_get_response_missing_text(self):
        with self.assertRaises(self.chatbot.ChatBotException):
            self.chatbot.get_response()
        # with_conversation
        with self.assertRaises(self.chatbot.ChatBotException):
            self.chatbot.get_response(conversation='test')

    def test_generate_response(self):
        statement = Statement(text='你想做什么')
        response = self.chatbot.generate_response(statement)

        self.assertEqual('你想做什么', statement.text)
        self.assertEqual(response.confidence, 0)

    def test_learn_response(self):
        previous_response = Statement(text='Define Hemoglobin.')
        statement = Statement(text='Hemoglobin is an oxygen-transport metalloprotein.')
        self.chatbot.learn_response(statement, previous_response)
        results = list(self.chatbot.storage.filter(text=statement.text))

        self.assertIsLength(results, 1)

    def test_get_response_does_not_add_new_statement(self):
        """
        Test that a new statement is not learned if `read_only` is set to True.
        """
        self.chatbot.read_only = True
        self.chatbot.get_response('早上好!')
        results = list(self.chatbot.storage.filter(text='早上好!'))

        self.assertIsLength(results, 0)

    def test_get_latest_response(self):
        # from_zero_responses
        response = self.chatbot.get_latest_response('invalid')
        self.assertIsNone(response)
        self.tearDown()

        # from_one_responses
        self.chatbot.storage.create(text='A', conversation='test')
        self.chatbot.storage.create(text='B', conversation='test', in_response_to='A')
        response = self.chatbot.get_latest_response('test')
        self.assertEqual(response.text, 'A')

        # from_two_responses
        self.chatbot.storage.create(text='C', conversation='test', in_response_to='B')
        response = self.chatbot.get_latest_response('test')
        self.assertEqual(response.text, 'B')

        # from_three_responses
        self.chatbot.storage.create(text='D', conversation='test', in_response_to='C')
        response = self.chatbot.get_latest_response('test')
        self.assertEqual(response.text, 'C')

    def test_search_text_results_after_training(self):
        """
        ChatterBot should return close matches to an input
        string when filtering using the search_text parameter.
        """
        self.chatbot.storage.create_many([
            Statement('Example A for search.'),
            Statement('Another example.'),
            Statement('Example B for search.'),
            Statement(text='Another statement.'),
        ])
        text = self.chatbot.storage.tagger.get_text_index_string('Example A for search.')
        results = list(self.chatbot.storage.filter(search_text=text))

        self.assertEqual(len(results), 1)
        self.assertEqual('Example A for search.', results[0].text)


