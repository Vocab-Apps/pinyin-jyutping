import unittest
import pytest
import pprint
import logging
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

logger = logging.getLogger(__file__)

import pinyin_jyutping
import pinyin_jyutping.parser
import pinyin_jyutping.data
import pinyin_jyutping.logic
import pinyin_jyutping.constants
import pinyin_jyutping.cache

from pinyin_jyutping.syllables import PinyinSyllable, JyutpingSyllable
from pinyin_jyutping.constants import PinyinInitials, PinyinFinals, PinyinTones
from pinyin_jyutping.constants import JyutpingInitials, JyutpingFinals, JyutpingTones

class JyutpingParsingTests(unittest.TestCase):
    def test_parse_syllables(self):
        test_list = [
            {'input': 'nin4', 'expected_syllable': JyutpingSyllable(JyutpingInitials.n, JyutpingFinals.in_, JyutpingTones.tone_4)},
            {'input': 'm4', 'expected_syllable': JyutpingSyllable(JyutpingInitials.empty, JyutpingFinals.m, JyutpingTones.tone_4)}
        ]

        for test in test_list:
            input = test['input']
            expected_syllable = test['expected_syllable']
            syllables = pinyin_jyutping.parser.parse_jyutping(input)
            self.assertEqual(len(syllables), 1)
            self.assertEqual(syllables[0], expected_syllable)            


    def test_parse_jyutping_cc_canto(self):
        filename = 'source_data/cccanto-webdist-160115.txt'
        for entry in pinyin_jyutping.parser.parse_cccanto_definition_generator(filename):
            jyutping = entry['jyutping']
            try:
                syllables = pinyin_jyutping.parser.parse_jyutping(jyutping)
            except pinyin_jyutping.errors.PinyinSyllableNotFound as e:
                logger.error(f'could not find syllable for {entry}, {e}')
                self.assertTrue(False)
