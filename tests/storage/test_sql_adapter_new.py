from unittest import TestCase
from app.chatterbot.conversation import Statement
from app.chatterbot.conversation import StatementRules
from app.chatterbot.storage.sql_storage_new import SQLStorageAdapterNew
from app.chatterbot import languages
#import unittest
class SQLStorageAdapterNewTestCase(TestCase):
    """
    SQL Storage Adapter New测试类
    """
    @classmethod
    def setUpClass(cls):
        """
        初始化database，采用sqlite，测试使用英文
        """
        cls.adapter = SQLStorageAdapterNew(database_uri=None, tagger_language=languages.CHI)

    def tearDown(self):
        """
        测试结束之后，删除数据库
        """
        self.adapter.drop()

class SQLStorageAdapterNewTests(SQLStorageAdapterNewTestCase):
    """
    具体测试SQL Storage Adapter New
    """
    def test_set_database_uri_none(self):
        adapter = SQLStorageAdapterNew(database_uri=None)
        self.assertEqual(adapter.database_uri, 'sqlite://')

    def test_set_database_uri(self):
        adapter = SQLStorageAdapterNew(database_uri='sqlite:///db.sqlite3')
        self.assertEqual(adapter.database_uri, 'sqlite:///db.sqlite3')

    def test_not_set_language(self):
        adapter = SQLStorageAdapterNew(database_uri=None)
        self.assertEqual(adapter.tagger.language, languages.ENG)

    def test_set_language(self):
        adapter = SQLStorageAdapterNew(database_uri=None, tagger_language=languages.CHI)
        self.assertEqual(adapter.tagger.language, languages.CHI)

    def test_count_by_name_returns_zero(self):
        self.assertEqual(self.adapter.count_by_name('statement'), 0)
        self.assertEqual(self.adapter.count_by_name('statementrules'), 0)

    def test_count_by_name_returns_not_zero(self):
        self.assertEqual(self.adapter.count_by_name('statement'), 0)
        self.adapter.create_text(text='this is a test.')
        self.assertEqual(self.adapter.count_by_name('statement'), 1)
        self.adapter.create_rule(text='hello!', in_response_to='how are you')
        self.assertEqual(self.adapter.count_by_name('statementrules'), 1)

    def test_filter_text_not_found(self):
        res = list(self.adapter.filter_text(id=1))
        self.assertEqual(len(res), 0)

    def test_filter_text_found(self):
        self.adapter.create_text(text='How are you?')
        res = list(self.adapter.filter_text(text='How are you?'))
        self.assertEqual(len(res),1)


    def test_filter_rules_not_found(self):
        res = list(self.adapter.filter_rules(id=1))
        self.assertEqual(len(res),0)

    def test_filter_rules_found(self):
        self.adapter.create_rule(id=1,text='How are you?',in_response_to='I am fine.')
        res = list(self.adapter.filter_rules(text='How are you?'))
        self.assertEqual(len(res),1)

    def test_update_text_add_new_statement(self):
        statement = Statement(text='How are you?')
        self.adapter.update_text(statement)
        res = list(self.adapter.filter_text(text=statement.text))
        self.assertEqual(len(res),1)
        self.assertEqual(res[0].text,statement.text)

    def test_update_text_modifies_existed_statement(self):
        self.adapter.create_text(text='How are you?')
        res = list(self.adapter.filter_text(text='How are you?'))
        self.assertEqual(len(res),1)
        self.assertEqual(res[0].in_response_to,None)
        statement = Statement(text='How are you?',in_response_to='I am fine.')
        self.adapter.update_text(statement)
        res = list(self.adapter.filter_text(text='How are you?'))
        self.assertEqual(len(res),1)
        self.assertEqual(res[0].in_response_to,statement.in_response_to)

    def test_update_rule_add_new_rule(self):
        statement = StatementRules(text="How are you?",in_response_to="I am fine.")
        self.adapter.update_rule(statement)
        res = list(self.adapter.filter_rules(text=statement.text))
        self.assertEqual(len(res),1)
        self.assertEqual(res[0].text,statement.text)

    def test_update_rule_modifies_existed_rule(self):
        self.adapter.create_rule(text="How are you?",in_response_to="I am fine.")
        res = list(self.adapter.filter_rules(text="How are you?"))
        self.assertEqual(len(res),1)
        self.assertEqual(res[0].in_response_to,"I am fine.")
        statement = StatementRules(text="How are you?", in_response_to="thank you.")
        self.adapter.update_rule(statement)
        res = list(self.adapter.filter_rules(text=statement.text))
        self.assertEqual(len(res),1)
        self.assertEqual(res[0].in_response_to,"thank you.")

    def test_remove_text_by_text(self):
        text = 'How are you?'
        self.adapter.create_text(text=text)
        self.adapter.remove_text_by_text(text)
        res = list(self.adapter.filter_text(text=text))
        self.assertEqual(len(res),0)

    def test_remove_text_by_id(self):
        text = 'How are you?'
        id = 1
        self.adapter.create_text(id=id,text=text)
        self.adapter.remove_text_by_id(id)
        res = list(self.adapter.filter_text(id=id))
        self.assertEqual(len(res),0)

    def test_remove_rule_by_text(self):
        text = "How are you?"
        in_response_to = "I am fine."
        id = 1
        self.adapter.create_rule(id=id,text=text,in_response_to=in_response_to)
        self.adapter.remove_rules_by_text(text)
        res = list(self.adapter.filter_rules(text=text))
        self.assertEqual(len(res),0)

    def test_remove_rule_by_id(self):
        text = "How are you?"
        in_response_to = "I am fine."
        id = 1
        self.adapter.create_rule(id=id, text=text, in_response_to=in_response_to)
        self.adapter.remove_rules_by_id(id)
        res = list(self.adapter.filter_rules(id=id))
        self.assertEqual(len(res), 0)

class SQLStorageAdapterNewFilterTests(SQLStorageAdapterNewTestCase):
    '''
    测试filter_text,filter_rule相关细节
    '''
    def test_filter_text_with_text_no_match(self):
        self.adapter.create_text(id=1,text='How are you?',in_response_to="I am fine.")
        res = list(self.adapter.filter_text(text='You are a gay.'))
        self.assertEqual(len(res),0)

    def test_filter_rules_with_text_no_match(self):
        self.adapter.create_rule(id=1,text='How are you?',in_response_to="I am fine.")
        res = list(self.adapter.filter_rules(text='You are a gay.'))
        self.assertEqual(len(res),0)

    def test_filter_text_with_id_no_match(self):
        self.adapter.create_text(id=1,text='How are you?',in_response_to="I am fine.")
        res = list(self.adapter.filter_text(id=2))
        self.assertEqual(len(res),0)

    def test_filter_rules_with_id_no_match(self):
        self.adapter.create_rule(id=1,text='How are you?',in_response_to="I am fine.")
        res = list(self.adapter.filter_rules(id=2))
        self.assertEqual(len(res),0)

    def test_filter_text_with_in_response_to_no_match(self):
        self.adapter.create_text(id=1,text='How are you?',in_response_to="I am fine.")
        res = list(self.adapter.filter_text(in_response_to="thank you"))
        self.assertEqual(len(res),0)

    def test_filter_rules_with_in_response_to_no_match(self):
        self.adapter.create_rule(id=1,text='How are you?',in_response_to="I am fine.")
        res = list(self.adapter.filter_rules(in_response_to="thank you"))
        self.assertEqual(len(res),0)

    def test_filter_text_with_equal_results(self):
        statement1 = Statement(
            text="Testing...",
            in_response_to=None
        )
        statement2 = Statement(
            text="Testing one, two, three.",
            in_response_to=None
        )
        self.adapter.update_text(statement1)
        self.adapter.update_text(statement2)
        res = list(self.adapter.filter_text(in_response_to=None))
        self.assertEqual(len(res),2)
        res_text = [
            result.text for result in res
        ]
        self.assertEqual(len(res_text), 2)
        self.assertIn(statement1.text, res_text)
        self.assertIn(statement2.text, res_text)

    def test_filter_rules_with_equal_results(self):
        statement1 = StatementRules(
            text="Testing...",
            in_response_to=None
        )
        statement2 = StatementRules(
            text="Testing one, two, three.",
            in_response_to=None
        )
        self.adapter.update_rule(statement1)
        self.adapter.update_rule(statement2)
        res = list(self.adapter.filter_rules(in_response_to=None))
        self.assertEqual(len(res),2)
        res_text = [
            result.text for result in res
        ]
        self.assertEqual(len(res_text), 2)
        self.assertIn(statement1.text, res_text)
        self.assertIn(statement2.text, res_text)


    def test_filter_text_with_no_parameter(self):
        self.adapter.create_text(text="Testing...")
        self.adapter.create_text(text="Testing one, two, three.")
        res = list(self.adapter.filter_text())
        self.assertEqual(len(res), 2)

    def test_filter_rules_with_no_parameter(self):
        self.adapter.create_rule(text="Testing...",in_response_to='yes!')
        self.adapter.create_rule(text="Testing one, two, three.",in_response_to='four!')
        res = list(self.adapter.filter_rules())
        self.assertEqual(len(res), 2)

    def test_filter_text_by_tag(self):
        self.adapter.create_text(text="Hello!", tags=["greeting", "salutation"])
        self.adapter.create_text(text="Hi everyone!", tags=["greeting", "exclamation"])
        self.adapter.create_text(text="The air contains Oxygen.", tags=["fact"])

        results = self.adapter.filter_text(tags=["greeting"])

        results_text_list = [statement.text for statement in results]

        self.assertEqual(len(results_text_list), 2)
        self.assertIn("Hello!", results_text_list)
        self.assertIn("Hi everyone!", results_text_list)

    def test_filter_text_by_tags(self):
        self.adapter.create_text(text="Hello!", tags=["greeting", "salutation"])
        self.adapter.create_text(text="Hi everyone!", tags=["greeting", "exclamation"])
        self.adapter.create_text(text="The air contains Oxygen.", tags=["fact"])

        results = self.adapter.filter_text(
            tags=["exclamation", "fact"]
        )

        results_text_list = [statement.text for statement in results]

        self.assertEqual(len(results_text_list), 2)
        self.assertIn("Hi everyone!", results_text_list)
        self.assertIn("The air contains Oxygen.", results_text_list)

    def test_filter_text_by_excluded_text(self):
        self.adapter.create_text(text='Hello!')
        self.adapter.create_text(text='Hi everyone!')

        results = list(self.adapter.filter_text(
            exclude_text=[
                'Hello!'
            ]
        ))

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].text, 'Hi everyone!')


    def test_filter_text_by_exclude_text_words(self):
        self.adapter.create_text(text='This is a good example.')
        self.adapter.create_text(text='This is a bad example.')
        self.adapter.create_text(text='This is a worse example.')

        results = list(self.adapter.filter_text(
            exclude_text_words=[
                'bad', 'worse'
            ]
        ))

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].text, 'This is a good example.')

    def test_filter_text_by_text_contains(self):
        self.adapter.create_text(text='Hello!', search_text='hello exclamation')
        self.adapter.create_text(text='Hi everyone!', search_text='hi everyone')

        results = list(self.adapter.filter_text(
            search_text_contains='everyone'
        ))

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].text, 'Hi everyone!')


    def test_filter_text_by_text_contains_return_multi_result(self):
        self.adapter.create_text(text='Hello!', search_text='hello exclamation')
        self.adapter.create_text(text='Hi everyone!', search_text='hi everyone')

        results = list(self.adapter.filter_text(
            search_text_contains='hello everyone'
        ))

        self.assertEqual(len(results), 2)

class SQLStorageAdapterNewCreateTests(SQLStorageAdapterNewTestCase):
    '''
    测试create_rule,create_text
    '''

    def test_create_text_text(self):
        self.adapter.create_text(text='testing')

        results = list(self.adapter.filter_text())

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].text, 'testing')


    def test_create_text_search_text(self):
        self.adapter.create_text(
            text='testing',
            search_text='test'
        )

        results = list(self.adapter.filter_text())

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].search_text, 'test')

    def test_create_rule_search_text(self):
        self.adapter.create_rule(id=1, text='How are you?', in_response_to='I am fine.',search_text='hello')
        res = list(self.adapter.filter_rules())
        self.assertEqual(len(res),1)
        self.assertEqual(res[0].search_text,'hello')

    def test_create_text_search_in_response_to(self):
        self.adapter.create_text(
            text='testing',
            search_in_response_to='test'
        )

        results = list(self.adapter.filter_text())

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].search_in_response_to, 'test')

    def test_create_rule_search_in_response_to(self):
        self.adapter.create_rule(id=1, text='How are you?', in_response_to='I am fine.',search_in_response_to='hello')
        res = list(self.adapter.filter_rules())
        self.assertEqual(len(res),1)
        self.assertEqual(res[0].search_in_response_to,'hello')

    def test_create_text_tags(self):
        self.adapter.create_text(text='testing', tags=['a', 'b'])

        results = list(self.adapter.filter_text())
        results[0]=self.adapter.Session().merge(results[0])
        self.assertEqual(len(results), 1)
        self.assertIn('a', results[0].get_tags())
        self.assertIn('b', results[0].get_tags())

    def test_create_text_duplicate_tags(self):
        """
        The storage adapter should not create a statement with tags
        that are duplicates.
        """
        self.adapter.create_text(text='testing', tags=['ab', 'ab'])

        results = list(self.adapter.filter_text())
        results[0]=self.adapter.Session().merge(results[0])
        self.assertEqual(len(results), 1)
        self.assertEqual(len(results[0].get_tags()), 1)
        self.assertEqual(results[0].get_tags(), ['ab'])


class SQLStorageAdapterNewUpdateTests(SQLStorageAdapterNewTestCase):
    '''
    测试update_text,update_rule
    '''
    def test_update_text_adds_tags(self):
        statement = self.adapter.create_text(text='Testing')
        statement.add_tags('a', 'b')
        self.adapter.update_text(statement)

        statements = list(self.adapter.filter_text())
        statements[0] =self.adapter.Session().merge(statements[0])
        self.assertEqual(len(statements), 1)
        self.assertIn('a', statements[0].get_tags())
        self.assertIn('b', statements[0].get_tags())

    def test_update_text_duplicate_tags(self):
        """
        The storage adapter should not update a statement with tags
        that are duplicates.
        """
        statement = self.adapter.create_text(text='Testing', tags=['ab'])
        statement.add_tags('ab')
        self.adapter.update_text(statement)
        statements = list(self.adapter.filter_text())

        statements[0] = self.adapter.Session().merge(statements[0])
        self.assertEqual(len(statements), 1)
        self.assertEqual(len(statements[0].get_tags()), 1)
        self.assertEqual(statements[0].get_tags(), ['ab'])
