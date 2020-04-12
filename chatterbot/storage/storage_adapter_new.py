import logging
from chatterbot import languages
from chatterbot.tagging import PosLemmaTagger


class StorageAdapterNew(object):
    '''
    基于WechatterBot需求的storage adapter抽象类接口
    '''

    def __init__(self, *args, **kwargs):
        '''
        初始化Storage Adapter
        '''
        self.logger = kwargs.get('logger', logging.getLogger(__name__))

        Tagger = kwargs.get('tagger', PosLemmaTagger)

        self.tagger = Tagger(language=kwargs.get(
            'tagger_language', languages.ENG
        ))

    def filter_text(self, **kwargs):
        '''
        对话查询
        '''
        raise self.AdapterMethodNotImplementedError(
            'The `filter_text` method is not implemented by this adapter.'
        )

    def filter_rules(self, **kwargs):
        '''
        对话规则查询
        '''
        raise self.AdapterMethodNotImplementedError(
            'The `filter_rules` method is not implemented by this adapter.'
        )

    def create_text(self, **kwargs):
        '''
        在Storage Adapter中创建一条新的对话
        '''
        raise self.AdapterMethodNotImplementedError(
            'The `create_text` method is not implemented by this adapter.'
        )

    def create_rule(self, **kwargs):
        '''
        在Storage Adapter中创建一条新的对话规则
        '''
        raise self.AdapterMethodNotImplementedError(
            'The `create_rule` method is not implemented by this adapter.'
        )

    def create_many_texts(self, statements):
        """
        在Storage Adapter中创建多条新的对话
        """
        raise self.AdapterMethodNotImplementedError(
            'The `create_many_texts` method is not implemented by this adapter.'
        )

    def create_many_rules(self, statements):
        """
        在Storage Adapter中创建多条新的对话规则
        """
        raise self.AdapterMethodNotImplementedError(
            'The `create_many_rules` method is not implemented by this adapter.'
        )

    def update_text(self, statement):
        """
        更新Storage Adapter中某个对话
        """
        raise self.AdapterMethodNotImplementedError(
            'The `update_text` method is not implemented by this adapter.'
        )

    def update_rule(self, statement):
        """
        更新Storage Adapter中某个对话规则
        """
        raise self.AdapterMethodNotImplementedError(
            'The `update_rule` method is not implemented by this adapter.'
        )

    def remove_text(self, statement_text):
        """
        删除对应的对话
        """
        raise self.AdapterMethodNotImplementedError(
            'The `remove_text` method is not implemented by this adapter.'
        )

    def remove_rule(self, statement_text):
        """
        删除对应的对话规则
        """
        raise self.AdapterMethodNotImplementedError(
            'The `remove_rule` method is not implemented by this adapter.'
        )

    def drop(self):
        """
        删库跑路
        """
        raise self.AdapterMethodNotImplementedError(
            'The `drop` method is not implemented by this adapter.'
        )

    class AdapterMethodNotImplementedError(NotImplementedError):
        """
        An exception to be raised when a storage adapter method has not been implemented.
        Typically this indicates that the method should be implement in a subclass.
        """
        pass
