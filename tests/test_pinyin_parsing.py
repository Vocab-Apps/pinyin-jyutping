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

from pinyin_jyutping.syllables import PinyinSyllable
from pinyin_jyutping.constants import PinyinInitials, PinyinFinals, PinyinTones

class PinyinParsingTests(unittest.TestCase):
    # test parsing of pinyin
    # ======================

    def verify_parsing(self, text, initial, final, tone, tone_mark_render, tone_number_render):
        syllable, remaining_text = pinyin_jyutping.parser.parse_romanization(text, pinyin_jyutping.cache.PinyinSyllablesMap, pinyin_jyutping.cache.PINYIN_SYLLABLE_MAX_LENGTH)
        expected_syllable = PinyinSyllable(initial, final, tone)
        self.assertEqual(syllable, expected_syllable)
        self.assertEqual(syllable.render_tone_mark(), tone_mark_render)
        self.assertEqual(syllable.render_tone_number(), tone_number_render)

    def test_parse_pinyin(self):
        text = 'mǎ'
        syllable, remaining_text = pinyin_jyutping.parser.parse_romanization(text, pinyin_jyutping.cache.PinyinSyllablesMap, pinyin_jyutping.cache.PINYIN_SYLLABLE_MAX_LENGTH)
        expected_syllable = PinyinSyllable(
            PinyinInitials.m, 
            PinyinFinals.a, 
            PinyinTones.tone_3)
        self.assertEqual(syllable, expected_syllable)
        self.assertEqual(syllable.render_tone_mark(), 'mǎ')
        self.assertEqual(syllable.render_tone_number(), 'ma3')

        text = 'xiē'
        syllable, remaining_text = pinyin_jyutping.parser.parse_romanization(text, pinyin_jyutping.cache.PinyinSyllablesMap, pinyin_jyutping.cache.PINYIN_SYLLABLE_MAX_LENGTH)
        expected_syllable = PinyinSyllable(PinyinInitials.x, PinyinFinals.ie, PinyinTones.tone_1)
        self.assertEqual(syllable, expected_syllable)
        self.assertEqual(syllable.render_tone_mark(), 'xiē')
        self.assertEqual(syllable.render_tone_number(), 'xie1')

        text = 'xie1'
        syllable, remaining_text = pinyin_jyutping.parser.parse_romanization(text, pinyin_jyutping.cache.PinyinSyllablesMap, pinyin_jyutping.cache.PINYIN_SYLLABLE_MAX_LENGTH)
        self.assertEqual(syllable, expected_syllable)

        self.verify_parsing('nǚ', PinyinInitials.n, PinyinFinals.v, PinyinTones.tone_3, 'nǚ', 'nü3')

    def test_pinyin_parsing_special_cases(self):
        self.verify_parsing('er4', PinyinInitials.empty, PinyinFinals.er, PinyinTones.tone_4, 'èr', 'er4')
        self.verify_parsing('a1', PinyinInitials.empty, PinyinFinals.a, PinyinTones.tone_1, 'ā', 'a1')

    def test_parse_pinyin_word(self):
        text = 'yi1 ge5 ban4'
        expected_output = [
            PinyinSyllable(PinyinInitials.empty, PinyinFinals.i, PinyinTones.tone_1),
            PinyinSyllable(PinyinInitials.g, PinyinFinals.e, PinyinTones.tone_neutral),
            PinyinSyllable(PinyinInitials.b, PinyinFinals.an, PinyinTones.tone_4),
        ]
        output = pinyin_jyutping.parser.parse_pinyin(text)
        self.assertEqual(output, expected_output)

    def test_parse_pinyin_word_list(self):
        entries = [
            {'text': 'nan2 wang4', 'expected_output': [
                PinyinSyllable(PinyinInitials.n, PinyinFinals.an, PinyinTones.tone_2),
                PinyinSyllable(PinyinInitials.empty, PinyinFinals.uang, PinyinTones.tone_4),
            ]},
            {
                'text': 'bùjǐn 。 。 。 ,   hái ...',
                'expected_output': [
                    PinyinSyllable(PinyinInitials.b, PinyinFinals.u, PinyinTones.tone_4),
                    PinyinSyllable(PinyinInitials.j, PinyinFinals.in_, PinyinTones.tone_3),
                    PinyinSyllable(PinyinInitials.h, PinyinFinals.ai, PinyinTones.tone_2),
                ]
            },
            {
                'text':'long2 teng2 hu3 yue4',
                'expected_output': [
                    PinyinSyllable(PinyinInitials.l, PinyinFinals.ong, PinyinTones.tone_2),
                    PinyinSyllable(PinyinInitials.t, PinyinFinals.eng, PinyinTones.tone_2),
                    PinyinSyllable(PinyinInitials.h, PinyinFinals.u, PinyinTones.tone_3),
                    PinyinSyllable(PinyinInitials.empty, PinyinFinals.ve, PinyinTones.tone_4),
                ]                
            }
        ]
        for entry in entries:
            output = pinyin_jyutping.parser.parse_pinyin(entry['text'])
            self.assertEqual(output, entry['expected_output'])


    def test_parse_pinyin_syllable_list(self):
        # expected_syllable
        entries = [
            {'text': 'yue4', 'expected_syllable': PinyinSyllable(PinyinInitials.empty, PinyinFinals.ve, PinyinTones.tone_4)},
            {'text': 'r5', 'expected_syllable': PinyinSyllable(PinyinInitials.empty, PinyinFinals.er, PinyinTones.tone_neutral)},
            {'text': 'lu:4', 'expected_syllable': PinyinSyllable(PinyinInitials.l, PinyinFinals.v, PinyinTones.tone_4)},
            {'text': 'e2', 'expected_syllable': PinyinSyllable(PinyinInitials.empty, PinyinFinals.e, PinyinTones.tone_2)},
            {'text': 'guan1', 'expected_syllable': PinyinSyllable(PinyinInitials.g, PinyinFinals.uan, PinyinTones.tone_1)},
            {'text': 'jiao1', 'expected_syllable': PinyinSyllable(PinyinInitials.j, PinyinFinals.iao, PinyinTones.tone_1)},
            {'text': 'que4', 'expected_syllable': PinyinSyllable(PinyinInitials.q, PinyinFinals.ve, PinyinTones.tone_4)},
            {'text': 'wu3', 'expected_syllable': PinyinSyllable(PinyinInitials.empty, PinyinFinals.u, PinyinTones.tone_3)},
            {'text': 'wei2', 'expected_syllable': PinyinSyllable(PinyinInitials.empty, PinyinFinals.ui, PinyinTones.tone_2)}
        ]
        for entry in entries:
            text = entry['text']
            expected_syllable = entry['expected_syllable']
            syllable, remaining_text = pinyin_jyutping.parser.parse_romanization(text, pinyin_jyutping.cache.PinyinSyllablesMap, pinyin_jyutping.cache.PINYIN_SYLLABLE_MAX_LENGTH)
            self.assertEqual(syllable, expected_syllable)


    def test_parse_pinyin_word_capitalized(self):
        text = 'Long2 feng4'
        expected_output = [
            PinyinSyllable(PinyinInitials.l, PinyinFinals.ong, PinyinTones.tone_2),
            PinyinSyllable(PinyinInitials.f, PinyinFinals.eng, PinyinTones.tone_4),
        ]
        output = pinyin_jyutping.parser.parse_pinyin(text)
        self.assertEqual(output, expected_output)


