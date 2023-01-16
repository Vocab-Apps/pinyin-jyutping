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
        # pytest tests/test_jyutping_conversion.py -k test_multiple_jyutping -s -rPP  --log-cli-level=INFO
        data = [
            {'chinese': '全身按摩', 'expected_jyutping': 'cyùnsān ônmō'},
            {'chinese': '我出去攞野食', 'expected_jyutping': 'ngǒ cēothêoi ló jěsik'},
            {'chinese': '賣野食又唔係賺大錢', 'expected_jyutping': 'maai jěsik jau m hai zaandaaicín'},
            {'chinese': '你想做，就照做', 'expected_jyutping': 'něi sóeng zou ， zauzîu zou'},
            {'chinese': '交定金', 'expected_jyutping': 'gāau denggām'},
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


    def test_load_anki_deck(self):
        # pytest tests/test_jyutping_conversion.py -k test_load_anki_deck -s -rPP  --log-cli-level=ERROR
        json_file_path = os.path.join(os.path.dirname(__file__), '..', 'source_data', 'cantonese_jyutping_anki_deck.json')
        f = open(json_file_path, 'r')
        test_data = json.load(f)
        f.close()
        matching_entries_tone_numbers = 0
        matching_entries_tone_marks = 0
        for entry in test_data:
            chinese = entry['Chinese']
            expected_jyutping_tone_numbers = entry['Jyutping_ToneNumbers']
            expected_jyutping_tone_marks = entry['Jyutping_ToneMarks']
            try:
                # try tone number conversion
                expected_syllables = pinyin_jyutping.parser.parse_jyutping(expected_jyutping_tone_numbers)
                actual_syllables = pinyin_jyutping.parser.parse_jyutping(self.pinyin_jyutping.jyutping(chinese, tone_numbers=True)[0])

                if expected_syllables == actual_syllables:
                    matching_entries_tone_numbers += 1

                # try tone mark conversion
                actual_jyutping_tone_marks = self.pinyin_jyutping.jyutping(chinese)[0]
                if expected_jyutping_tone_marks == actual_jyutping_tone_marks:
                    matching_entries_tone_marks += 1
                else:
                    logger.error(f'tone marks not matching: actual: [{actual_jyutping_tone_marks}] expected: [{expected_jyutping_tone_marks}] chinese: [{chinese}]')

            except  pinyin_jyutping.errors.PinyinSyllableNotFound as e:
                logger.warning(e)

        self.assertGreater(matching_entries_tone_numbers, 3758)
        self.assertGreater(matching_entries_tone_marks, 2313)
