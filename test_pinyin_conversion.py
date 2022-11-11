import unittest
import pinyin_jyutping

"""this file contains final end-to-end conversion tests on real data"""
class PinyinConversion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pinyin_jyutping = pinyin_jyutping.PinyinJyutping()

    def test_1(self):
        self.assertEqual(self.pinyin_jyutping.pinyin('没有'), 'mei2you3')
