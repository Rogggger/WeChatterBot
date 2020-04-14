import os
import io
from unittest import TestCase
from chatterbot import corpus

LANGUAGES = ('english', 'chinese')

class CorpusTestCase(TestCase):
    def test_load_corpus(self):
        """
        Test loading the entire corpus of languages.
        """
        corpus_files = corpus.list_corpus_files('chatterbot.corpus')
        corpus_data = corpus.load_corpus(*corpus_files)
        self.assertTrue(len(list(corpus_data)))

    def test_load_corpus_language(self):
        for language in LANGUAGES:
            paths = [
                f'chatterbot.corpus.{language}',
                os.path.join(corpus.DATA_DIRECTORY, 'english') + '/',
                os.path.join(corpus.DATA_DIRECTORY, language)
            ]
            for file_path in paths:
                data_files = corpus.list_corpus_files(file_path)
                corpus_data = corpus.load_corpus(*data_files)
                self.assertGreater(len(list(corpus_data)), 1)

    def test_load_corpus_categories(self):
        # english - greetings
        data_files = corpus.list_corpus_files('chatterbot.corpus.english.greetings')
        corpus_data = list(corpus.load_corpus(*data_files))

        self.assertEqual(len(corpus_data), 1)
        for _conversation, categories, _file_path in corpus_data:
            self.assertIn('greetings', categories)

        conversations, categories, file_path = corpus_data[0]
        self.assertIn(['Hi', 'Hello'], conversations)
        self.assertEqual(['greetings'], categories)
        self.assertIn('chatterbot_corpus/data/english/greetings.yml', file_path)

    def test_load_corpus_greetings(self):
        for language in LANGUAGES:
            file_path = os.path.join(corpus.DATA_DIRECTORY, language, 'greetings.yml')
            data_files = corpus.list_corpus_files(file_path)
            corpus_data = corpus.load_corpus(*data_files)
            self.assertEqual(len(list(corpus_data)), 1)

    def test_get_file_path(self):
        """
        Test that a dotted path is properly converted to a file address.
        """
        for language in LANGUAGES:
            path = corpus.get_file_path(f'chatterbot.corpus.{language}')
            self.assertIn(
                os.path.join('chatterbot_corpus', 'data', language),
                path
            )

    def test_read_corpus(self):
        for language in LANGUAGES:
            corpus_path = os.path.join(
                corpus.DATA_DIRECTORY,
                language,
                'conversations.yml'
            )
            data = corpus.read_corpus(corpus_path)
            self.assertIn('conversations', data)

    def test_list_corpus_files(self):
        for language in LANGUAGES:
            data_files = corpus.list_corpus_files(f'chatterbot.corpus.{language}')
            for data_file in data_files:
                self.assertIn('.yml', data_file)

    def test_load_new_corpus_file(self):
        """
        Test that a file path can be specified for a corpus.
        """
        # Create a file for testing
        file_path = './test_corpus.yml'
        with io.open(file_path, 'w') as test_corpus:
            yml_data = u'\n'.join(
                ['conversations:', '- - Hello', '  - Hi', '- - Hi', '  - Hello']
            )
            test_corpus.write(yml_data)

        data_files = corpus.list_corpus_files(file_path)
        corpus_data = list(corpus.load_corpus(*data_files))

        # Remove the test file
        if os.path.exists(file_path):
            os.remove(file_path)

        self.assertEqual(len(corpus_data), 1)

        # Load the content from the corpus
        conversations, _categories, _file_path = corpus_data[0]

        self.assertEqual(len(conversations[0]), 2)

    def test_load_corpus_file_non_existent(self):
        """
        Test that a file path can be specified for a corpus.
        """
        file_path = './test_corpus.yml'
        self.assertFalse(os.path.exists(file_path))
        with self.assertRaises(IOError):
            list(corpus.load_corpus(file_path))
