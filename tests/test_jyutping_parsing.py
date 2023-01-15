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

class JyutpingParsingTests(unittest.TestCase):
    def test_parse_jyutping_cc_canto(self):
        filename = 'source_data/cccanto-webdist-160115.txt'
        for entry in pinyin_jyutping.parser.parse_cccanto_definition_generator(filename):
            jyutping = entry['jyutping']
            syllables = pinyin_jyutping.parser.parse_jyutping(jyutping)