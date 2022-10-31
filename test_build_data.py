
import pinyin_jyutping
import pinyin_jyutping.parser
import unittest

class BuildTests(unittest.TestCase):
    def test_1(self):
        text = 'mǎ'
        syllable = pinyin_jyutping.parser.parse_pinyin(text)
        expected_syllable = pinyin_jyutping.syllables.PinyinSyllable(
            pinyin_jyutping.constants.PinyinInitials.m, 
            pinyin_jyutping.constants.PinyinFinals.a, 
            pinyin_jyutping.constants.PinyinTones.tone_3)
        self.assertEqual(syllable, expected_syllable)
        self.assertEqual(syllable.render_tone_mark(), 'mǎ')
        self.assertEqual(syllable.render_tone_number(), 'ma3')

if __name__ == '__main__':
    main()