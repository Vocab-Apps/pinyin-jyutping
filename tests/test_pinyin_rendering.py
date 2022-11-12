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

from pinyin_jyutping.syllables import PinyinSyllable
from pinyin_jyutping.constants import PinyinInitials, PinyinFinals, PinyinTones

class PinyinRenderingTests(unittest.TestCase):
    # rendering of syllables to pinyin
    # ================================

    def test_render_syllables_tone_number(self):
        #  pytest test_build_data.py -k test_render_syllables_tone_number
        entries = [
            { 'syllable': PinyinSyllable(PinyinInitials.empty, PinyinFinals.e, PinyinTones.tone_2, capital=True), 'pinyin': 'E2'},
            { 'syllable': PinyinSyllable(PinyinInitials.q, PinyinFinals.ve, PinyinTones.tone_4), 'pinyin': 'que4'},
            # empty + u group tests
            { 'syllable': PinyinSyllable(PinyinInitials.empty, PinyinFinals.u, PinyinTones.tone_4), 'pinyin': 'wu4'},
            { 'syllable': PinyinSyllable(PinyinInitials.empty, PinyinFinals.ua, PinyinTones.tone_4), 'pinyin': 'wa4'},
            { 'syllable': PinyinSyllable(PinyinInitials.empty, PinyinFinals.uo, PinyinTones.tone_4), 'pinyin': 'wo4'},
            { 'syllable': PinyinSyllable(PinyinInitials.empty, PinyinFinals.uai, PinyinTones.tone_4), 'pinyin': 'wai4'},
            { 'syllable': PinyinSyllable(PinyinInitials.empty, PinyinFinals.ui, PinyinTones.tone_4), 'pinyin': 'wei4'},
            { 'syllable': PinyinSyllable(PinyinInitials.empty, PinyinFinals.uan, PinyinTones.tone_4), 'pinyin': 'wan4'},
            { 'syllable': PinyinSyllable(PinyinInitials.empty, PinyinFinals.uang, PinyinTones.tone_4), 'pinyin': 'wang4'},
            { 'syllable': PinyinSyllable(PinyinInitials.empty, PinyinFinals.un, PinyinTones.tone_4), 'pinyin': 'wen4'},
            { 'syllable': PinyinSyllable(PinyinInitials.empty, PinyinFinals.ueng, PinyinTones.tone_4), 'pinyin': 'weng4'},
            # empty + i group finals
            { 'syllable': PinyinSyllable(PinyinInitials.empty, PinyinFinals.i, PinyinTones.tone_4), 'pinyin': 'yi4'},
            { 'syllable': PinyinSyllable(PinyinInitials.empty, PinyinFinals.ia, PinyinTones.tone_4), 'pinyin': 'ya4'},
        ]
        for entry in entries:
            syllable = entry['syllable']
            expected_pinyin = entry['pinyin']
            pinyin = syllable.render_tone_number()
            self.assertEqual(pinyin, expected_pinyin)

    def test_render_syllables_tone_mark(self):
        entries = [
            { 'syllable': PinyinSyllable(PinyinInitials.n, PinyinFinals.v, PinyinTones.tone_3), 'pinyin': 'nǚ'},
            # empty + u group finals
            { 'syllable': PinyinSyllable(PinyinInitials.empty, PinyinFinals.u, PinyinTones.tone_4), 'pinyin': 'wù'},
            { 'syllable': PinyinSyllable(PinyinInitials.empty, PinyinFinals.ua, PinyinTones.tone_4), 'pinyin': 'wà'},
            { 'syllable': PinyinSyllable(PinyinInitials.empty, PinyinFinals.uo, PinyinTones.tone_4), 'pinyin': 'wò'},
            { 'syllable': PinyinSyllable(PinyinInitials.empty, PinyinFinals.uai, PinyinTones.tone_4), 'pinyin': 'wài'},
            { 'syllable': PinyinSyllable(PinyinInitials.empty, PinyinFinals.ui, PinyinTones.tone_4), 'pinyin': 'wèi'},
            { 'syllable': PinyinSyllable(PinyinInitials.empty, PinyinFinals.uan, PinyinTones.tone_4), 'pinyin': 'wàn'},
            { 'syllable': PinyinSyllable(PinyinInitials.empty, PinyinFinals.un, PinyinTones.tone_4), 'pinyin': 'wèn'},
            { 'syllable': PinyinSyllable(PinyinInitials.empty, PinyinFinals.ueng, PinyinTones.tone_4), 'pinyin': 'wèng'},
            { 'syllable': PinyinSyllable(PinyinInitials.empty, PinyinFinals.uang, PinyinTones.tone_4), 'pinyin': 'wàng'},
            # empty + i group finals
            { 'syllable': PinyinSyllable(PinyinInitials.empty, PinyinFinals.i, PinyinTones.tone_4), 'pinyin': 'yì'},
            { 'syllable': PinyinSyllable(PinyinInitials.empty, PinyinFinals.ia, PinyinTones.tone_4), 'pinyin': 'yà'},
            { 'syllable': PinyinSyllable(PinyinInitials.empty, PinyinFinals.ie, PinyinTones.tone_4), 'pinyin': 'yè'},
            { 'syllable': PinyinSyllable(PinyinInitials.empty, PinyinFinals.iao, PinyinTones.tone_4), 'pinyin': 'yào'},
            { 'syllable': PinyinSyllable(PinyinInitials.empty, PinyinFinals.iu, PinyinTones.tone_4), 'pinyin': 'yòu'},
            { 'syllable': PinyinSyllable(PinyinInitials.empty, PinyinFinals.ian, PinyinTones.tone_4), 'pinyin': 'yàn'},
            { 'syllable': PinyinSyllable(PinyinInitials.empty, PinyinFinals.iang, PinyinTones.tone_4), 'pinyin': 'yàng'},
            { 'syllable': PinyinSyllable(PinyinInitials.empty, PinyinFinals.in_, PinyinTones.tone_4), 'pinyin': 'yìn'},
            { 'syllable': PinyinSyllable(PinyinInitials.empty, PinyinFinals.ing, PinyinTones.tone_4), 'pinyin': 'yìng'},
            { 'syllable': PinyinSyllable(PinyinInitials.empty, PinyinFinals.iong, PinyinTones.tone_4), 'pinyin': 'yòng'},
        ]
        for entry in entries:
            syllable = entry['syllable']
            expected_pinyin = entry['pinyin']
            pinyin = syllable.render_tone_mark()
            self.assertEqual(pinyin, expected_pinyin)            

    def test_render_final_variant(self):
        self.assertEqual(pinyin_jyutping.logic.render_tone_number(PinyinInitials.empty, 
            PinyinFinals.er, 
            PinyinTones.tone_neutral, 
            False),
            'er5')
        self.assertEqual(pinyin_jyutping.logic.render_tone_number(PinyinInitials.empty, 
            PinyinFinals.er, 
            PinyinTones.tone_neutral, 
            False,
            'r'),
            'r5')                