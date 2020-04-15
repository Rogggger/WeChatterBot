"""
Test ChatterBot's statement comparison algorithms.
"""

from unittest import TestCase
from app.chatterbot_api.chatterbot.conversation import Statement
from app.chatterbot_api.chatterbot import comparisons
from app.chatterbot_api.chatterbot import languages

# set language
LANGUAGE = languages.ENG

class LevenshteinDistanceTestCase(TestCase):
    def setUp(self):
        self.compare = comparisons.LevenshteinDistance(language=LANGUAGE)

    def test_false(self):
        """
        Falsy values should match by zero.
        """
        # Test first statement is empty
        statement = Statement(text='')
        other_statement = Statement(text='Hello')
        value = self.compare(statement, other_statement)
        self.assertEqual(value, 0)

        # Test latter statement is empty
        statement = Statement(text='Hello')
        other_statement = Statement(text='')
        value = self.compare(statement, other_statement)
        self.assertEqual(value, 0)

        # Test that an exception is not raised
        # if a statement is initialized with an integer value as its text attribute.
        statement = Statement(text=2)
        other_statement = Statement(text='Hello')
        value = self.compare(statement, other_statement)
        self.assertEqual(value, 0)

    def test_true(self):
        # Test that text capitalization is ignored.
        statement = Statement(text='Hi HoW ArE yOu?')
        other_statement = Statement(text='hI hOw are YoU?')
        value = self.compare(statement, other_statement)
        self.assertEqual(value, 1)


class SpacySimilarityTests(TestCase):
    def setUp(self):
        self.compare = comparisons.LevenshteinDistance(language=LANGUAGE)

    def test_true(self):
        # Test sentences with different stopwords.
        statement = Statement(text='What is matter?')
        other_statement = Statement(text='What is the matter?')
        value = self.compare(statement, other_statement)
        self.assertAlmostEqual(value, 0.9, places=1)

        # Test that text capitalization is ignored.
        statement = Statement(text='Hi HoW ArE yOu?')
        other_statement = Statement(text='hI hOw are YoU?')
        value = self.compare(statement, other_statement)
        self.assertAlmostEqual(value, 1, places=1)


class JaccardSimilarityTestCase(TestCase):
    def setUp(self):
        self.compare = comparisons.LevenshteinDistance(language=LANGUAGE)

    def test_true(self):
        # Test that text capitalization is ignored.
        statement = Statement(text='Hi HoW ArE yOu?')
        other_statement = Statement(text='hI hOw are YoU?')
        value = self.compare(statement, other_statement)
        self.assertEqual(value, 1)
