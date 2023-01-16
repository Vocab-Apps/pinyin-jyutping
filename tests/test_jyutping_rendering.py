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

from pinyin_jyutping.syllables import JyutpingSyllable
from pinyin_jyutping.constants import JyutpingInitials, JyutpingFinals, JyutpingTones

class JyutpingRenderingTests(unittest.TestCase):

    def test_render_syllables_tone_number(self):
        entries = [
            { 'syllable': JyutpingSyllable(JyutpingInitials.n, JyutpingFinals.in_, JyutpingTones.tone_4), 'jyutping': 'nin4'},
        ]
        for entry in entries:
            syllable = entry['syllable']
            expected_jyutping = entry['jyutping']
            pinyin = syllable.render_tone_number()
            self.assertEqual(pinyin, expected_jyutping)

    def test_render_syllables_tone_mark(self):
        entries = [
            { 'syllable': JyutpingSyllable(JyutpingInitials.n, JyutpingFinals.in_, JyutpingTones.tone_4), 'jyutping': 'nìn'},
        ]
        for entry in entries:
            syllable = entry['syllable']
            expected_jyutping = entry['jyutping']
            jyutping = syllable.render_tone_mark()
            self.assertEqual(jyutping, expected_jyutping)
