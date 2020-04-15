from tests.base_case import ChatBotTestCase
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement

class ChatterBotResponseTestCase(ChatBotTestCase):
    def test_conversation_values_persisted_to_response(self):
        response = self.chatbot.get_response(
            'Hello',
            persist_values_to_response={'conversation': 'test 1 你好'}
        )
        self.assertEqual(response.conversation, 'test 1 你好')

    def test_tag_values_persisted_to_response(self):
        response = self.chatbot.get_response(
            'Hello',
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

    def test_statement_known_response_cases(self):
        """
        number of statements known -- number of responses
        """
        # 0 -- 0
        # If there is no statements in the database,
        # then the user's input is the only thing that can be returned.
        statement_text = '你好吗？'
        response = self.chatbot.get_response(statement_text)
        results = list(self.chatbot.storage.filter(text=statement_text))
        self.assertEqual(response.text, statement_text)
        self.assertEqual(response.confidence, 0)
        self.assertIsLength(results, 2)
        self.assertEqual(results[0].text, statement_text)
        self.assertEqual(results[1].text, statement_text)
        self.tearDown()

        # 1 -- 0
        self.chatbot.storage.create(text='Hello', in_response_to=None)
        response = self.chatbot.get_response('Hi')
        self.assertEqual(response.confidence, 0)
        self.assertEqual(response.text, 'Hello')
        self.tearDown()

        # 1 -- 1
        self.chatbot.storage.create(text='Hello', in_response_to='Hi')
        response = self.chatbot.get_response('Hi')
        self.assertEqual(response.confidence, 0)
        self.assertEqual(response.text, 'Hello')

        # 2 -- 1
        self.chatbot.storage.create(text='Hi', in_response_to=None)
        response = self.chatbot.get_response('Hi')
        self.assertEqual(response.confidence, 1)
        self.assertEqual(response.text, 'Hello')

        # 3 -- 2
        self.chatbot.storage.create(text='How are you?', in_response_to='Hello')
        first_response = self.chatbot.get_response('Hi')
        second_response = self.chatbot.get_response('How are you?')
        # self.assertEqual(first_response.confidence, 1)
        # self.assertEqual(first_response.text, 'Hello')
        self.assertEqual(second_response.confidence, 0)

        # 4 -- 3
        self.chatbot.storage.create(text='I am well.', in_response_to='How are you?')
        first_response = self.chatbot.get_response('Hi')
        second_response = self.chatbot.get_response('How are you?')
        # self.assertEqual(first_response.confidence, 1)
        # self.assertEqual(first_response.text, 'Hello')
        self.assertEqual(second_response.confidence, 1)
        self.assertEqual(second_response.text, 'I am well.')


    def test_second_response_unknown(self):
        self.chatbot.storage.create(text='Hi', in_response_to=None)
        self.chatbot.storage.create(text='Hello', in_response_to='Hi')

        first_response = self.chatbot.get_response(
            text='Hi',
            conversation='test'
        )
        second_response = self.chatbot.get_response(
            text='How are you?',
            conversation='test'
        )

        results = list(self.chatbot.storage.filter(text='How are you?'))

        self.assertEqual(first_response.confidence, 1)
        self.assertEqual(first_response.text, 'Hello')
        self.assertEqual(first_response.in_response_to, 'Hi')

        self.assertEqual(second_response.confidence, 0)
        self.assertEqual(second_response.in_response_to, 'How are you?')

        # Make sure that the second response was saved to the database
        self.assertIsLength(results, 1)
        self.assertEqual(results[0].in_response_to, 'Hi')

    def test_statement_added_to_conversation(self):
        """
        An input statement should be added to the recent response list.
        """
        statement = Statement(text='Wow!', conversation='test')
        response = self.chatbot.get_response(statement)

        self.assertEqual(statement.text, response.text)
        self.assertEqual(response.conversation, 'test')

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

        # Test the case that a non-whitespace C1 control string is passed in.
        response = self.chatbot.get_response(u'')
        self.assertGreater(len(response.text), 0)

        # Test the case that a string containing two-byte characters is passed in.
        response = self.chatbot.get_response(u'田中さんにあげて下さい')
        self.assertGreater(len(response.text), 0)

        # Test the case that a string contains "corrupted" text.
        response = self.chatbot.get_response(u'Ṱ̺̺̕h̼͓̲̦̳̘̲e͇̣̰̦̬͎ ̢̼̻̱̘h͚͎͙̜̣̲ͅi̦̲̣̰̤v̻͍e̺̭̳̪̰-m̢iͅn̖̺̞̲̯̰d̵̼̟͙̩̼̘̳.̨̹͈̣')
        self.assertGreater(len(response.text), 0)

    def test_response_with_tags_added(self):
        """
        If an input statement has tags added to it,
        that data should saved with the input statement.
        """
        self.chatbot.get_response(
            Statement(
                text='Hello',
                in_response_to='Hi',
                tags=['test']
            )
        )
        results = list(self.chatbot.storage.filter(text='Hello'))

        self.assertIsLength(results, 2)
        self.assertIn('test', results[0].get_tags())
        self.assertEqual(results[1].get_tags(), [])

    def test_get_response_with_text_and_kwargs(self):
        self.chatbot.get_response('Hello', conversation='greetings')

        results = list(self.chatbot.storage.filter(text='Hello'))

        self.assertIsLength(results, 2)
        self.assertEqual(results[0].conversation, 'greetings')
        self.assertEqual(results[1].conversation, 'greetings')

    def test_get_response_missing_text(self):
        with self.assertRaises(self.chatbot.ChatBotException):
            self.chatbot.get_response()
        # with_conversation
        with self.assertRaises(self.chatbot.ChatBotException):
            self.chatbot.get_response(conversation='test')

    def test_generate_response(self):
        statement = Statement(text='Many insects adopt a tripedal gait for rapid yet stable walking.')
        response = self.chatbot.generate_response(statement)

        self.assertEqual(response.text, statement.text)
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
        self.chatbot.get_response('Hi!')
        results = list(self.chatbot.storage.filter(text='Hi!'))

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



class ChatBotLogicAdapterTestCase(ChatBotTestCase):
    texts = (
        ('Good morning.', 0.2),
        ('Good morning.', 0.5),
        ('Good night.', 0.7),
    )
    @classmethod
    def process(cls, index):
        response = Statement(text=cls.texts[index][0])
        response.confidence = cls.texts[index][1]
        return response

    class TestAdapterA(LogicAdapter):
        def process(self, statement, additional_response_selection_parameters=None):
            return ChatBotLogicAdapterTestCase.process(0)
    class TestAdapterB(LogicAdapter):
        def process(self, statement, additional_response_selection_parameters=None):
            return ChatBotLogicAdapterTestCase.process(1)
    class TestAdapterC(LogicAdapter):
        def process(self, statement, additional_response_selection_parameters=None):
            return ChatBotLogicAdapterTestCase.process(2)

    def test_sub_adapter_agreement(self):
        """
        In the case that multiple adapters agree on a given
        statement, this statement should be returned with the
        highest confidence available from these matching options.
        """
        self.chatbot.logic_adapters = [
            self.TestAdapterA(self.chatbot),
            self.TestAdapterB(self.chatbot),
            self.TestAdapterC(self.chatbot)
        ]
        statement = self.chatbot.generate_response(Statement(text='Howdy!'))

        self.assertEqual(statement.confidence, 0.5)
        self.assertEqual(statement.text, 'Good morning.')

    def test_chatbot_set_for_all_logic_adapters(self):
        for sub_adapter in self.chatbot.logic_adapters:
            self.assertEqual(sub_adapter.chatbot, self.chatbot)
        self.assertGreater(
            len(self.chatbot.logic_adapters), 0,
            msg='At least one logic adapter is expected for this test.'
        )

    def test_response_persona_is_bot(self):
        """
        The response returned from the chatbot should be set to the name of the chatbot.
        """
        response = self.chatbot.get_response('Hey everyone!')
        self.assertEqual(response.persona, 'bot:Test Bot')
