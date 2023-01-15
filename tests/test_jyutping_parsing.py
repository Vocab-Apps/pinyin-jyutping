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
            {'input': 'm4', 'expected_syllable': JyutpingSyllable(JyutpingInitials.empty, JyutpingFinals.m, JyutpingTones.tone_4)},
            {'input': 'laang5', 'expected_syllable': JyutpingSyllable(JyutpingInitials.l, JyutpingFinals.aang, JyutpingTones.tone_5)}
        ]

        for test in test_list:
            input = test['input']
            expected_syllable = test['expected_syllable']
            rendered_tone_numbers = expected_syllable.render_tone_number()
            print(rendered_tone_numbers)
            syllables = pinyin_jyutping.parser.parse_jyutping(input)
            self.assertEqual(len(syllables), 1)
            self.assertEqual(syllables[0], expected_syllable)            


    def test_parse_jyutping_cc_canto(self):
        filename = 'source_data/cccanto-webdist-160115.txt'
        matched_entries = 0
        for entry in pinyin_jyutping.parser.parse_cccanto_definition_generator(filename):
            jyutping = entry['jyutping']
            try:
                syllables = pinyin_jyutping.parser.parse_jyutping(jyutping)
                jyutping_tone_numbers = ' '.join([syllable.render_tone_number() for syllable in syllables])
                # now parse again based on what we rendered
                parsed_syllables = pinyin_jyutping.parser.parse_jyutping(jyutping_tone_numbers)
                self.assertEqual(len(syllables), len(parsed_syllables))
                self.assertEqual(syllables, parsed_syllables)
                matched_entries += 1
            except pinyin_jyutping.errors.PinyinSyllableNotFound as e:
                logger.error(f'could not find syllable for {entry}, {e}')
                # self.assertTrue(False)

        self.assertGreater(matched_entries, 22326)

    def test_parse_jyutping_ccedit_canto_readings(self):
        filename = 'source_data/cccedict-canto-readings-150923.txt'
        matched_entries = 0
        for entry in pinyin_jyutping.parser.parse_cccedit_canto_readings_generator(filename):
            jyutping = entry['jyutping']
            try:
                syllables = pinyin_jyutping.parser.parse_jyutping(jyutping)
                jyutping_tone_numbers = ' '.join([syllable.render_tone_number() for syllable in syllables])
                # now parse again based on what we rendered
                parsed_syllables = pinyin_jyutping.parser.parse_jyutping(jyutping_tone_numbers)
                self.assertEqual(len(syllables), len(parsed_syllables))
                self.assertEqual(syllables, parsed_syllables)
                matched_entries += 1
            except pinyin_jyutping.errors.PinyinSyllableNotFound as e:
                logger.error(f'could not find syllable for {entry}, {e}')
                # self.assertTrue(False)

        self.assertGreater(matched_entries, 105816)
