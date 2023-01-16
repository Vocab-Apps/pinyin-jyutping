import unittest
import pytest
import sys
import os
import json
import pprint
import requests
import logging

logger = logging.getLogger(__file__)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pinyin_jyutping
import pinyin_jyutping.parser
import pinyin_jyutping.errors

"""this file contains final end-to-end conversion tests on real data"""
class JyutpingConversion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        cls.pinyin_jyutping = pinyin_jyutping.PinyinJyutping()


    def test_simple_jyutping(self):
        self.assertEqual(self.pinyin_jyutping.jyutping('全身按摩'), ['cyùnsān ônmō'])

    def test_multiple_jyutping(self):
        data = [
            {'chinese': '全身按摩', 'expected_jyutping': 'cyùnsān ônmō'},
            {'chinese': '我出去攞野食', 'expected_jyutping': 'ngǒ cēothêoi ló jěsik'},
        ]

        for entry in data:
            chinese = entry['chinese']
            expected_jyutping = entry['expected_jyutping']
            self.assertEqual(self.pinyin_jyutping.jyutping(chinese)[0], expected_jyutping)
    