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

    def test_tone_changes(self):
        self.assertEqual(self.pinyin_jyutping.pinyin('穿不上')[0], 'chuān bú shàng')
        self.assertEqual(self.pinyin_jyutping.pinyin('不够亮')[0], 'búgòu liàng')
        self.assertEqual(self.pinyin_jyutping.pinyin('不成熟')[0], 'bù chéngshú')
        # dosen't seem to be applied by azure
        # self.assertEqual(self.pinyin_jyutping.pinyin('一起')[0], 'yìqǐ')
        self.assertEqual(self.pinyin_jyutping.pinyin('一个')[0], 'yígè')

    def get_baserow_records(self):
        more_results = True

        records = []

        url = "https://api.baserow.io/api/database/rows/table/114466/?user_field_names=true&size=200"
        while more_results == True:
            logger.info(f'get_baserow_records querying url {url}')
            # load baserow table
            response = requests.get(
                url,
                headers={
                    "Authorization": f"Token {os.environ['BASEROW_API_TOKEN']}"
            })
            if response.status_code != 200:
                raise Exception(response.content)
            data = response.json()

            results = data['results']
            logger.info(f'received {len(results)} records')
            records.extend(results)

            more_results = data['next'] != None
            url = data['next']

        return records

    def get_baserow_records_map(self):
        records = self.get_baserow_records()
        result = {}
        for record in records:
            result[record['chinese']] = record
        return result


    def update_baserow_records(self, records):
        response = requests.patch(
            "https://api.baserow.io/api/database/rows/table/114466/batch/?user_field_names=true",
            headers={
                "Authorization": f"Token {os.environ['BASEROW_API_TOKEN']}",
                "Content-Type": "application/json"
            },
            json={
                "items": records
            }        
        )
        if response.status_code != 200:
            raise Exception(response.content)


    @pytest.mark.skipif('COMPARE_ANKI_DECKS' not in os.environ, reason="set COMPARE_ANKI_DECKS=yes")
    def test_compare_anki_decks(self):
        # COMPARE_ANKI_DECKS=yes BASEROW_API_TOKEN=<api token> 
        # pytest tests/test_pinyin_conversion.py -k test_compare_anki_decks -s -rPP  --log-cli-level=INFO
        filename = 'source_data/anki_deck_1.json'
        f = open(filename)
        data = json.load(f)
        f.close()

        baserow_record_map = self.get_baserow_records_map()
        record_updates = []

        for record in data:
            chinese = record['chinese']
            expected_pinyin = pinyin_jyutping.parser.clean_pinyin(record['pinyin'])
            converted_pinyin = pinyin_jyutping.parser.clean_pinyin(self.pinyin_jyutping.pinyin(chinese, spaces=True)[0])

            try:
                expected_pinyin_syllables = pinyin_jyutping.parser.parse_pinyin_word(expected_pinyin)
                converted_pinyin_syllables = pinyin_jyutping.parser.parse_pinyin_word(converted_pinyin)

                status = 313817 # failure
                if expected_pinyin_syllables == converted_pinyin_syllables:
                    status = 313816 # success

                record_updates.append({
                    'id': baserow_record_map[chinese]['id'],
                    'expected_pinyin': expected_pinyin,
                    'expected_syllables': str(expected_pinyin_syllables),
                    'converted_pinyin': converted_pinyin,
                    'converted_pinyin_syllables': str(converted_pinyin_syllables),
                    'status': status
                })            

            except pinyin_jyutping.errors.PinyinParsingError as e:
                logger.error(e)

            if len(record_updates) >= 100:
                logger.info('flushing baserow updates')
                # flush to baserow
                self.update_baserow_records(record_updates)
                record_updates = []
                
