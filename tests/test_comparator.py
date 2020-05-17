"""
Test ChatterBot's statement comparison algorithms.
"""

from unittest import TestCase
from app.chatterbot.conversation import Statement
from app.chatterbot import comparisons
from app.chatterbot import languages, tagging

# set language
LANGUAGE = languages.CHI


class LevenshteinDistanceTestCase(TestCase):
    def setUp(self):
        self.compare = comparisons.LevenshteinDistance(language=LANGUAGE)

    def test_false(self):
        """
        Falsy values should match by zero.
        """
        # Test first statement is empty
        statement = Statement(text='')
        other_statement = Statement(text='你好')
        value = self.compare(statement, other_statement)
        self.assertEqual(value, 0)

        # Test latter statement is empty
        statement = Statement(text='你好')
        other_statement = Statement(text='')
        value = self.compare(statement, other_statement)
        self.assertEqual(value, 0)

        # Test that an exception is not raised
        # if a statement is initialized with an integer value as its text attribute.
        statement = Statement(text=2)
        other_statement = Statement(text='你好')
        value = self.compare(statement, other_statement)
        self.assertEqual(value, 0)

    def test_true(self):
        # Test that text capitalization is ignored.
        statement = Statement(text='你好今天怎么样')
        other_statement = Statement(text='你好今天怎么样')
        value = self.compare(statement, other_statement)
        self.assertEqual(value, 1)


class SpacySimilarityTests(TestCase):
    def setUp(self):
        self.compare = comparisons.LevenshteinDistance(language=LANGUAGE)

    def test_false(self):
        """
        Falsy values should match by zero.
        """
        # Test first statement is empty
        statement = Statement(text='')
        other_statement = Statement(text='你好')
        value = self.compare(statement, other_statement)
        self.assertEqual(value, 0)

        # Test latter statement is empty
        statement = Statement(text='你好')
        other_statement = Statement(text='')
        value = self.compare(statement, other_statement)
        self.assertEqual(value, 0)

        # Test that an exception is not raised
        # if a statement is initialized with an integer value as its text attribute.
        statement = Statement(text=2)
        other_statement = Statement(text='你好')
        value = self.compare(statement, other_statement)
        self.assertEqual(value, 0)

    def test_true(self):
        # Test sentences with different stopwords.
        statement = Statement(text='今天天气怎么样')
        other_statement = Statement(text='今天天气怎么样啊')
        value = self.compare(statement, other_statement)
        self.assertAlmostEqual(value, 0.9, places=1)

        # Test that text capitalization is ignored.
        statement = Statement(text='你好')
        other_statement = Statement(text='你好')
        value = self.compare(statement, other_statement)
        self.assertAlmostEqual(value, 1, places=1)


class JaccardSimilarityTestCase(TestCase):
    def setUp(self):
        self.compare = comparisons.LevenshteinDistance(language=LANGUAGE)
        self.tagger = tagging.PosLemmaTagger(language=LANGUAGE)

    def test_false(self):
        """
        Falsy values should match by zero.
        """
        # Test first statement is empty
        statement = Statement(text='', search_text=self.tagger.get_text_index_string(''))
        other_statement = Statement(text='你好', search_text=self.tagger.get_text_index_string('你好'))
        value = self.compare(statement, other_statement)
        self.assertEqual(value, 0)

        # Test latter statement is empty
        statement = Statement(text='你好', search_text=self.tagger.get_text_index_string('你好'))
        other_statement = Statement(text='', search_text=self.tagger.get_text_index_string(''))
        value = self.compare(statement, other_statement)
        self.assertEqual(value, 0)

        # Test that an exception is not raised
        # if a statement is initialized with an integer value as its text attribute.
        statement = Statement(text=2)
        other_statement = Statement(text='你好')
        value = self.compare(statement, other_statement)
        self.assertEqual(value, 0)

    def test_true(self):
        # Test that text capitalization is ignored.
        text = '你好'
        statement = Statement(text=text, search_text=self.tagger.get_text_index_string(text))
        other_text = '你好'
        other_statement = Statement(text=other_text, search_text=self.tagger.get_text_index_string(other_text))
        value = self.compare(statement, other_statement)
        self.assertEqual(value, 1)
