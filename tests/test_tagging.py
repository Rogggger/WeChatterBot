from unittest import TestCase
from app.chatterbot import languages
from app.chatterbot import tagging


class PosLemmaTaggerTests(TestCase):

    def setUp(self):
        self.tagger = tagging.PosLemmaTagger(language=languages.CHI)

    def test_empty_string(self):
        tagged_text = self.tagger.get_text_index_string(
            ''
        )

        self.assertEqual(tagged_text, '')

    def test_tagging(self):
        tagged_text = self.tagger.get_text_index_string(
            '你喜欢音乐吗'
        )

        self.assertEqual(tagged_text, '喜欢 音乐')

    def test_tagging_chinese(self):
        self.tagger = tagging.PosLemmaTagger(
            language=languages.CHI
        )

        tagged_text = self.tagger.get_text_index_string(
            '你喜欢音乐吗'
        )

        self.assertEqual(tagged_text, '喜欢 音乐')

    # TODO test failed

    def test_tagging_long_words(self):
        tagged_text = self.tagger.get_text_index_string('我会很多种乐器，是不是很厉害')

        self.assertEqual(tagged_text, '我会 多种 乐器 厉害')

    def test_get_text_index_string_punctuation_only(self):
        bigram_string = self.tagger.get_text_index_string(
            '?'
        )

        self.assertEqual(bigram_string, '?')

    def test_get_text_index_string_single_character(self):
        bigram_string = self.tagger.get_text_index_string(
            ''
        )

        self.assertEqual(bigram_string, '')

    def test_get_text_index_string_bigram_word(self):
        bigram_string = self.tagger.get_text_index_string('你好')

        self.assertEqual(bigram_string, '你好')
