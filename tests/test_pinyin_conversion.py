import unittest
import pytest
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

    def test_simple_chars(self):
        self.assertEqual(self.pinyin_jyutping.pinyin('忘'), ['wàng'])

    # @pytest.mark.skip(reason="too many alternatives")
    def test_pinyin_sentences(self):
        self.assertEqual(self.pinyin_jyutping.pinyin('忘拿一些东西了')[0], 'wàng ná yīxiē dōngxī le')
        self.assertEqual(self.pinyin_jyutping.pinyin('忘拿一些东西了', tone_numbers=True)[0], 'wang4 na2 yi1xie1 dong1xi1 le5')
        self.assertEqual(self.pinyin_jyutping.pinyin('忘拿一些东西了', tone_numbers=True, spaces=True)[0], 'wang4 na2 yi1 xie1 dong1 xi1 le5')
