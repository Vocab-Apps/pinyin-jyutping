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
        # pytest tests/test_jyutping_conversion.py -s -rPP  --log-cli-level=INFO
        data = [
            {'chinese': '全身按摩', 'expected_jyutping': 'cyùnsān ônmō'},
            {'chinese': '我出去攞野食', 'expected_jyutping': 'ngǒ cēothêoi ló jěsik'},
            {'chinese': '賣野食又唔係賺大錢', 'expected_jyutping': 'maai jěsik jau m hai zaandaaicín'},
            {'chinese': '你想做，就照做', 'expected_jyutping': 'něi sóeng zou ， zauzîu zou'},
        ]

        for entry in data:
            chinese = entry['chinese']
            expected_jyutping = entry['expected_jyutping']
            self.assertEqual(self.pinyin_jyutping.jyutping(chinese)[0], expected_jyutping)
    

    def test_user_corrections(self):
        # apply corrections
        pinyin_jyutping_instance_1 = pinyin_jyutping.PinyinJyutping()
        pinyin_jyutping_instance_1.load_jyutping_corrections(
            [
                {
                    'chinese': '按摩',
                    'jyutping': 'on1mo1'
                }
            ]
        )
        self.assertEqual(pinyin_jyutping_instance_1.jyutping('全身按摩')[0], 'cyùnsān ōnmō')