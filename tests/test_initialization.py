from tests.base_case import ChatBotTestCase

from app.chatterbot_api.chatterbot.storage import SQLStorageAdapter as Storage
from app.chatterbot_api.chatterbot.logic import BestMatch as Logic_1
from app.chatterbot_api.chatterbot.logic import MathematicalEvaluation as Logic_2

Storage_path = f'chatterbot.storage.{Storage.__name__}'
Logic_1_path = f'chatterbot.logic.{Logic_1.__name__}'
Logic_2_path = f'chatterbot.logic.{Logic_2.__name__}'

Keyword_string = {
    'storage_adapter': Storage_path,
    'database_uri': None,
    'logic_adapters': [Logic_1_path, Logic_2_path]
}
Keyword_dict = {
    'storage_adapter': {
        'import_path': Storage_path,
        'database_uri': None
    },
    'logic_adapters': [
        {'import_path': Logic_1_path},
        {'import_path': Logic_2_path},
    ]
}

class StringInitializationTestCase(ChatBotTestCase):
    @property
    def kwargs(self):
        return Keyword_string

    def test_storage_initialized(self):
        self.assertTrue(isinstance(self.chatbot.storage, Storage))

    def test_logic_initialized(self):
        self.assertEqual(len(self.chatbot.logic_adapters), 2)
        self.assertTrue(isinstance(self.chatbot.logic_adapters[0], Logic_1))

class DictionaryInitializationTestCase(ChatBotTestCase):
    @property
    def kwargs(self):
        return Keyword_dict

    def test_storage_initialized(self):
        self.assertTrue(isinstance(self.chatbot.storage, Storage))

    def test_logic_initialized(self):
        self.assertEqual(len(self.chatbot.logic_adapters), 2)
        self.assertTrue(isinstance(self.chatbot.logic_adapters[0], Logic_1))
        self.assertTrue(isinstance(self.chatbot.logic_adapters[1], Logic_2))
