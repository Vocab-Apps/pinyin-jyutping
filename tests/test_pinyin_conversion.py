import unittest
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pinyin_jyutping

"""this file contains final end-to-end conversion tests on real data"""
class PinyinConversion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        cls.pinyin_jyutping = pinyin_jyutping.PinyinJyutping()

    def test_character_conversion(self):
        self.assertEqual(self.pinyin_jyutping.pinyin('了'), ['le', 'liǎo', 'liào'])

    def test_simple_pinyin(self):
        self.assertEqual(self.pinyin_jyutping.pinyin('没有'), ['méiyǒu'])
        # self.assertEqual(self.pinyin_jyutping.pinyin('忘拿'), ['wàng ná'])

    def test_simple_pinyin_traditional(self):
        self.assertEqual(self.pinyin_jyutping.pinyin('上課'), ['shàngkè'])

    def test_pinyin_non_recognized_chars(self):
        # pytest --log-cli-level=DEBUG tests/test_pinyin_conversion.py -k test_pinyin_non_recognized_chars
        self.assertEqual(self.pinyin_jyutping.pinyin('請問，你叫什麼名字？')[0], 'qǐngwèn ， nǐ jiào shénme míngzi ？')
        # self.assertEqual(self.pinyin_jyutping.pinyin('請問，你叫什麼名字？'), ['qǐngwèn ， nǐ jiào shénme míngzì ？'])

    def test_simple_chars(self):
        self.assertEqual(self.pinyin_jyutping.pinyin('忘'), ['wàng'])

    # @pytest.mark.skip(reason="too many alternatives")
    def test_pinyin_sentences(self):
        self.assertEqual(self.pinyin_jyutping.pinyin('忘拿一些东西了')[0], 'wàng ná yīxiē dōngxi le')
        self.assertEqual(self.pinyin_jyutping.pinyin('忘拿一些东西了', tone_numbers=True)[0], 'wang4 na2 yi1xie1 dong1xi5 le5')
        self.assertEqual(self.pinyin_jyutping.pinyin('忘拿一些东西了', tone_numbers=True, spaces=True)[0], 'wang4 na2 yi1 xie1 dong1 xi5 le5')
