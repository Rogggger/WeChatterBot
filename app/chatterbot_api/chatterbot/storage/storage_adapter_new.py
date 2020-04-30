import logging
from app.chatterbot_api.chatterbot import languages
from app.chatterbot_api.chatterbot.tagging import PosLemmaTagger


class StorageAdapterNew(object):
    """
    基于WechatterBot需求的storage adapter抽象类接口
    """

    def __init__(self, *args, **kwargs):
        """
        根据参数初始化Storage Adapter
        """
        self.logger = kwargs.get('logger', logging.getLogger(__name__))

        Tagger = kwargs.get('tagger', PosLemmaTagger)

        self.tagger = Tagger(language=kwargs.get(
            'tagger_language', languages.ENG
        ))

    def get_model(self, model_name):
        """
        Return the model class for a given model name.

        model_name is case insensitive.
        """
        get_model_method = getattr(self, 'get_%s_model' % (
            model_name.lower(),
        ))

        return get_model_method()

    def get_object(self, object_name):
        """
        Return the class for a given object name.

        object_name is case insensitive.
        """
        get_model_method = getattr(self, 'get_%s_object' % (
            object_name.lower(),
        ))

        return get_model_method()

    def get_statement_object(self):
        from app.chatterbot_api.chatterbot.conversation import Statement

        StatementModel = self.get_model('statement')

        Statement.statement_field_names.extend(
            StatementModel.extra_statement_field_names
        )

        return Statement

    def count(self, search_table):
        """
        Return the number of entries in the search table.
        """
        raise self.AdapterMethodNotImplementedError(
            'The `count` method is not implemented by this adapter.'
        )

    def filter_text(self, **kwargs):
        """
        对话查询
        """
        raise self.AdapterMethodNotImplementedError(
            'The `filter_text` method is not implemented by this adapter.'
        )

    def filter_text_by_text(self, statement_text):
        """
        对话查询,通过text查找
        """
        raise self.AdapterMethodNotImplementedError(
            'The `filter_text_by_text` method is not implemented by this adapter.'
        )

    def filter_rules(self, **kwargs):
        """
        对话规则查询
        """
        raise self.AdapterMethodNotImplementedError(
            'The `filter_rules` method is not implemented by this adapter.'
        )

    def filter_rules_by_text(self, rule_text):
        """
        对话规则查询
        """
        raise self.AdapterMethodNotImplementedError(
            'The `filter_rules_by_text` method is not implemented by this adapter.'
        )

    def create_text(self, **kwargs):
        """
        在Storage Adapter中创建一条新的对话
        """
        raise self.AdapterMethodNotImplementedError(
            'The `create_text` method is not implemented by this adapter.'
        )

    def create_rule(self, **kwargs):
        """
        在Storage Adapter中创建一条新的对话规则
        """
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

    def remove_text(self,**kwargs):
        """
        删除对应的对话
        """
        raise self.AdapterMethodNotImplementedError(
            'The `remove_text` method is not implemented by this adapter.'
        )

    def remove_text_by_text(self, statement_text):
        """
        删除对应的对话,根据text删除
        """
        raise self.AdapterMethodNotImplementedError(
            'The `remove_text_by_text` method is not implemented by this adapter.'
        )

    def remove_text_by_id(self, statement_id):
        """
        删除对应的对话,根据id删除
        """
        raise self.AdapterMethodNotImplementedError(
            'The `remove_text_by_id` method is not implemented by this adapter.'
        )

    def remove_rule(self, **kwargs):
        """
        删除对应的对话规则
        """
        raise self.AdapterMethodNotImplementedError(
            'The `remove_rule` method is not implemented by this adapter.'
        )

    def remove_rule_by_text(self, rule_text):
        """
        删除对应的对话规则，根据对话删除
        """
        raise self.AdapterMethodNotImplementedError(
            'The `remove_rule_by_text` method is not implemented by this adapter.'
        )

    def remove_rule_by_id(self, rule_id):
        """
        删除对应的对话规则，根据id删除
        """
        raise self.AdapterMethodNotImplementedError(
            'The `remove_rule_by_id` method is not implemented by this adapter.'
        )

    def drop(self):
        """
        删库跑路
        """
        raise self.AdapterMethodNotImplementedError(
            'The `drop` method is not implemented by this adapter.'
        )

    class EmptyDatabaseException(Exception):

        def __init__(self, message=None):
            default = 'The database currently contains no entries. At least one entry is expected. You may need to train your chat bot to populate your database.'
            super().__init__(message or default)

    class AdapterMethodNotImplementedError(NotImplementedError):
        """
        An exception to be raised when a storage adapter method has not been implemented.
        Typically this indicates that the method should be implement in a subclass.
        """
        pass
