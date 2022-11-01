
import pinyin_jyutping
import pinyin_jyutping.parser
import unittest

from pinyin_jyutping.syllables import PinyinSyllable
from pinyin_jyutping.constants import PinyinInitials, PinyinFinals, PinyinTones

class BuildTests(unittest.TestCase):
    def verify_parsing(self, text, initial, final, tone, tone_mark_render, tone_number_render):
        syllable = pinyin_jyutping.parser.parse_pinyin(text)
        expected_syllable = PinyinSyllable(initial, final, tone)
        self.assertEqual(syllable, expected_syllable)
        self.assertEqual(syllable.render_tone_mark(), tone_mark_render)
        self.assertEqual(syllable.render_tone_number(), tone_number_render)

    def test_1(self):
        text = 'mǎ'
        syllable = pinyin_jyutping.parser.parse_pinyin(text)
        expected_syllable = PinyinSyllable(
            PinyinInitials.m, 
            PinyinFinals.a, 
            PinyinTones.tone_3)
        self.assertEqual(syllable, expected_syllable)
        self.assertEqual(syllable.render_tone_mark(), 'mǎ')
        self.assertEqual(syllable.render_tone_number(), 'ma3')

        text = 'xiē'
        syllable = pinyin_jyutping.parser.parse_pinyin(text)
        expected_syllable = PinyinSyllable(PinyinInitials.x, PinyinFinals.ie, PinyinTones.tone_1)
        self.assertEqual(syllable, expected_syllable)
        self.assertEqual(syllable.render_tone_mark(), 'xiē')
        self.assertEqual(syllable.render_tone_number(), 'xie1')

        text = 'xie1'
        syllable = pinyin_jyutping.parser.parse_pinyin(text)
        self.assertEqual(syllable, expected_syllable)

        self.verify_parsing('nǚ', PinyinInitials.n, PinyinFinals.v, PinyinTones.tone_3, 'nǚ', 'nv3')

    def test_show_pinyin_finals(self):
        print(len(PinyinFinals))
        print(list(PinyinFinals))


if __name__ == '__main__':
    main()