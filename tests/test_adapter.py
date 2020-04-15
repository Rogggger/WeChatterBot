from tests.base_case import ChatBotTestCase
from app.chatterbot_api.chatterbot import ChatBot
from app.chatterbot_api.chatterbot.adapters import Adapter

def get_kwargs():
    return {
        # Run the test database in-memory
        'database_uri': None,
        # Don't execute initialization processes such as downloading required data
        'initialize': False
    }

class AdapterValidationTests(ChatBotTestCase):
    def test_invalid_storage_adapter(self):
        kwargs = get_kwargs()
        kwargs['storage_adapter'] = 'chatterbot.logic.LogicAdapter'
        with self.assertRaises(Adapter.InvalidAdapterTypeException):
            self.chatbot = ChatBot('Test Bot', **kwargs)

    def test_valid_storage_adapter(self):
        kwargs = get_kwargs()
        kwargs['storage_adapter'] = 'chatterbot.storage.SQLStorageAdapter'
        try:
            self.chatbot = ChatBot('Test Bot', **kwargs)
        except Adapter.InvalidAdapterTypeException:
            self.fail('Test raised InvalidAdapterException unexpectedly!')

    def test_invalid_logic_adapter(self):
        kwargs = get_kwargs()
        kwargs['logic_adapters'] = ['chatterbot.storage.StorageAdapter']
        with self.assertRaises(Adapter.InvalidAdapterTypeException):
            self.chatbot = ChatBot('Test Bot', **kwargs)

    def test_valid_logic_adapter(self):
        kwargs = get_kwargs()
        kwargs['logic_adapters'] = ['chatterbot.logic.BestMatch']
        try:
            self.chatbot = ChatBot('Test Bot', **kwargs)
        except Adapter.InvalidAdapterTypeException:
            self.fail('Test raised InvalidAdapterException unexpectedly!')

    def test_valid_adapter_dictionary(self):
        kwargs = get_kwargs()
        kwargs['storage_adapter'] = {'import_path': 'chatterbot.storage.SQLStorageAdapter'}
        try:
            self.chatbot = ChatBot('Test Bot', **kwargs)
        except Adapter.InvalidAdapterTypeException:
            self.fail('Test raised InvalidAdapterException unexpectedly!')

    def test_invalid_adapter_dictionary(self):
        kwargs = get_kwargs()
        kwargs['storage_adapter'] = {'import_path': 'chatterbot.logic.BestMatch'}
        with self.assertRaises(Adapter.InvalidAdapterTypeException):
            self.chatbot = ChatBot('Test Bot', **kwargs)
