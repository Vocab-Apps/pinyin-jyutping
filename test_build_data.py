
import pinyin_jyutping
import pinyin_jyutping.parser
import unittest
import pytest

from pinyin_jyutping.syllables import PinyinSyllable
from pinyin_jyutping.constants import PinyinInitials, PinyinFinals, PinyinTones

class BuildTests(unittest.TestCase):
    def verify_parsing(self, text, initial, final, tone, tone_mark_render, tone_number_render):
        syllable, remaining_text = pinyin_jyutping.parser.parse_pinyin(text)
        expected_syllable = PinyinSyllable(initial, final, tone)
        self.assertEqual(syllable, expected_syllable)
        self.assertEqual(syllable.render_tone_mark(), tone_mark_render)
        self.assertEqual(syllable.render_tone_number(), tone_number_render)

    def test_1(self):
        text = 'mǎ'
        syllable, remaining_text = pinyin_jyutping.parser.parse_pinyin(text)
        expected_syllable = PinyinSyllable(
            PinyinInitials.m, 
            PinyinFinals.a, 
            PinyinTones.tone_3)
        self.assertEqual(syllable, expected_syllable)
        self.assertEqual(syllable.render_tone_mark(), 'mǎ')
        self.assertEqual(syllable.render_tone_number(), 'ma3')

        text = 'xiē'
        syllable, remaining_text = pinyin_jyutping.parser.parse_pinyin(text)
        expected_syllable = PinyinSyllable(PinyinInitials.x, PinyinFinals.ie, PinyinTones.tone_1)
        self.assertEqual(syllable, expected_syllable)
        self.assertEqual(syllable.render_tone_mark(), 'xiē')
        self.assertEqual(syllable.render_tone_number(), 'xie1')

        text = 'xie1'
        syllable, remaining_text = pinyin_jyutping.parser.parse_pinyin(text)
        self.assertEqual(syllable, expected_syllable)

        self.verify_parsing('nǚ', PinyinInitials.n, PinyinFinals.v, PinyinTones.tone_3, 'nǚ', 'nv3')

    def test_special_cases(self):
        self.verify_parsing('er4', PinyinInitials.er, PinyinFinals.er, PinyinTones.tone_4, 'èr', 'er4')

    def test_parse_pinyin_word(self):
        text = 'yi1 ge5 ban4'
        expected_output = [
            PinyinSyllable(PinyinInitials.y, PinyinFinals.i, PinyinTones.tone_1),
            PinyinSyllable(PinyinInitials.g, PinyinFinals.e, PinyinTones.tone_neutral),
            PinyinSyllable(PinyinInitials.b, PinyinFinals.an, PinyinTones.tone_4),
        ]
        output = pinyin_jyutping.parser.parse_pinyin_word(text)
        self.assertEqual(output, expected_output)

    @pytest.mark.skip(reason="wait until parsing is more advanced")
    def test_load_cedict(self):
        filename = 'source_data/cedict_1_0_ts_utf-8_mdbg.txt'
        pinyin_jyutping.parser.parse_cedict(filename)



if __name__ == '__main__':
    main()