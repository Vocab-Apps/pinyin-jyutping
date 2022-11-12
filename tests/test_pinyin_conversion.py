import unittest
import pytest
import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pinyin_jyutping
import pinyin_jyutping.parser
import pinyin_jyutping.errors

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
        self.assertEqual(self.pinyin_jyutping.pinyin('請問，你叫什麼名字？'), 
            ['qǐngwèn ， nǐ jiào shénme míngzi ？',
            'qǐngwèn ， nǐ jiào shénme míngzì ？',])

    def test_simple_chars(self):
        self.assertEqual(self.pinyin_jyutping.pinyin('忘'), ['wàng'])

    # @pytest.mark.skip(reason="too many alternatives")
    def test_pinyin_sentences(self):
        self.assertEqual(self.pinyin_jyutping.pinyin('忘拿一些东西了')[0], 'wàng ná yīxiē dōngxi le')
        self.assertEqual(self.pinyin_jyutping.pinyin('忘拿一些东西了', tone_numbers=True)[0], 'wang4 na2 yi1xie1 dong1xi5 le5')
        self.assertEqual(self.pinyin_jyutping.pinyin('忘拿一些东西了', tone_numbers=True, spaces=True)[0], 'wang4 na2 yi1 xie1 dong1 xi5 le5')


    @pytest.mark.skip(reason="work in progress")
    def test_compare_anki_decks(self):
        filename = 'source_data/anki_deck_1.json'
        f = open(filename)
        data = json.load(f)
        f.close()

        success_count = 0
        failure_count = 0

        error_records = []

        for record in data:
            chinese = record['chinese']
            expected_pinyin = record['pinyin']
            converted_pinyin = self.pinyin_jyutping.pinyin(chinese)[0]

            try:
                expected_pinyin_syllables = pinyin_jyutping.parser.parse_pinyin_word(expected_pinyin)
                converted_pinyin_syllables = pinyin_jyutping.parser.parse_pinyin_word(converted_pinyin)

                # self.assertEqual(expected_pinyin_syllables, converted_pinyin_syllables, f'{chinese}, {expected_pinyin}, {converted_pinyin}')
                if expected_pinyin_syllables == converted_pinyin_syllables:
                    success_count += 1
                else:
                    error_records.append({
                        'expected_pinyin': expected_pinyin,
                        'expected_syllables': str(expected_pinyin_syllables),
                        'converted_pinyin': converted_pinyin,
                        'converted_pinyin_syllables': str(converted_pinyin_syllables)
                    })
                    failure_count += 1
            except pinyin_jyutping.errors.PinyinParsingError as e:
                failure_count += 1

        import pandas

        errors_df = pandas.DataFrame(error_records)
        errors_df.to_csv('source_data/anki_deck_errors.csv')

        self.assertEqual(failure_count, 0, f'success: {success_count}, failures: {failure_count}')

            # print(record)
