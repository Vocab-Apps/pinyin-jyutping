import pinyin_jyutping
import pinyin_jyutping.parser
import pinyin_jyutping.data
import pinyin_jyutping.logic
import pinyin_jyutping.constants
import pickle
import unittest
import pytest
import pprint
import logging
import re

logger = logging.getLogger(__file__)

from pinyin_jyutping.syllables import PinyinSyllable
from pinyin_jyutping.constants import PinyinInitials, PinyinFinals, PinyinTones

class BuildTests(unittest.TestCase):



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

    # conversion tests
    # ================

    def build_data_from_input(self, input_data):
        data = pinyin_jyutping.data.Data()
        for entry in input_data:
            chinese, pinyin = entry
            syllables = pinyin_jyutping.parser.parse_pinyin_word(pinyin)
            pinyin_jyutping.parser.process_word(chinese, syllables, data)
        return data

    def test_convert_pinyin_char(self):
        data = self.build_data_from_input([('没', 'mei2')])
        self.assertEqual(pinyin_jyutping.conversion.convert_pinyin(data, '没', True, False), ['mei2'])
        self.assertEqual(pinyin_jyutping.conversion.convert_pinyin(data, '没', False, False), ['méi'])

    def test_convert_pinyin_char_multiple_choice(self):
        data = self.build_data_from_input([
            ('没', 'mei2'),
            ('没', 'mei3'),
            ('没', 'mei2'),
        ])
        self.assertEqual(pinyin_jyutping.conversion.convert_pinyin(data, '没', True, False), ['mei2', 'mei3'])
        self.assertEqual(pinyin_jyutping.conversion.convert_pinyin(data, '没', False, False), ['méi', 'měi'])

    def test_convert_pinyin(self):
        input_data = [
            ('没有', 'mei2 you3')
        ]
        data = self.build_data_from_input(input_data)

        # no spaces    
        self.assertEqual(pinyin_jyutping.conversion.convert_pinyin(data, '没有', True, False), ['mei2you3'])
        # spaces
        self.assertEqual(pinyin_jyutping.conversion.convert_pinyin(data, '没有', True, True), ['mei2 you3'])

    def test_convert_pinyin_multiple_alternatives(self):
        input_data = [
            ('没有', 'mei2 you3'),
            ('没有', 'mei2 you3'),
            ('没有', 'mei2 you4'),
        ]
        data = self.build_data_from_input(input_data)

        # no spaces    
        self.assertEqual(pinyin_jyutping.conversion.convert_pinyin(data, '没有', True, False), ['mei2you3', 'mei2you4'])

    def test_convert_pinyin_words(self):
        input_data = [
            ('没有', 'mei2 you3'),
            ('什么', 'shen2 me5'),
        ]
        data = self.build_data_from_input(input_data)    
        self.assertEqual(pinyin_jyutping.conversion.convert_pinyin(data, '没有什么', True, False), ['mei2you3 shen2me5'])

    def test_convert_pinyin_sentences(self):
        input_data = [
            ('忘', 'wang4'),
            ('拿', 'na2'),
            ('一些', 'yīxiē'),
            ('东西', 'dōngxi'),
            ('了', 'le'),
        ]
        data = self.build_data_from_input(input_data)    
        self.assertEqual(pinyin_jyutping.conversion.convert_pinyin(data, '忘拿一些东西了', True, False)[0], 'wang4 na2 yi1xie1 dong1xi5 le5')


    # pickle / data storage tests
    # ===========================


    def test_dump_load_pickle(self):
        data = pinyin_jyutping.data.Data()
        lines = [
            '上周 上周 [shang4 zhou1] /last week/',
            '誰 谁 [shei2] /who/also pr. [shui2]/',
            '誰知 谁知 [shei2 zhi1] /who would have thought/unexpectedly/',
            '阿誰 阿谁 [a1 shui2] /who/',
            '不准 不准 [bu4 zhun3] /not to allow/to forbid/to prohibit/'
        ]
        pinyin_jyutping.parser.parse_cedict_entries(lines, data)

        pickled_data = pickle.dumps(data)

        unpickled_data = pickle.loads(pickled_data)


    @pytest.mark.skip(reason="still experimenting with pickle")
    def test_save_pickle(self):
        data = pinyin_jyutping.data.Data()
        sample_data_only = False
        if sample_data_only:
            lines = [
                '誰 谁 [shei2] /who/also pr. [shui2]/',
                '誰知 谁知 [shei2 zhi1] /who would have thought/unexpectedly/',
                '阿誰 阿谁 [a1 shui2] /who/',
                '不准 不准 [bu4 zhun3] /not to allow/to forbid/to prohibit/'
            ]
            pinyin_jyutping.parser.parse_cedict_entries(lines, data)
        else:
            filename = 'source_data/cedict_1_0_ts_utf-8_mdbg.txt'
            pinyin_jyutping.parser.parse_cedict(filename, data)            
        data_file = open('pinyin.pkl', 'wb')
        pickle.dump(data, data_file)
        data_file.close()
    
    @pytest.mark.skip(reason="still experimenting with pickle")
    def test_load_pickle(self):
        data_file = open('pinyin.pkl', 'rb')
        data = pickle.load(data_file)
        data_file.close()


    # CEDICT parsing related functions
    # ================================

    def test_parse_cedict(self):
        line = '上周 上周 [shang4 zhou1] /last week/'
        simplified, traditional, syllables = pinyin_jyutping.parser.parse_cedict_line(line)
        self.assertEqual(simplified, '上周')
        self.assertEqual(traditional, '上周')
        self.assertEqual(syllables, [
            PinyinSyllable(PinyinInitials.sh, PinyinFinals.ang, PinyinTones.tone_4),
            PinyinSyllable(PinyinInitials.zh, PinyinFinals.ou, PinyinTones.tone_1),            
        ])

    def test_build_data_cedict(self):
        data = pinyin_jyutping.data.Data()
        lines = [
            '誰 谁 [shei2] /who/also pr. [shui2]/',
            '誰知 谁知 [shei2 zhi1] /who would have thought/unexpectedly/',
            '阿誰 阿谁 [a1 shui2] /who/',
            '不准 不准 [bu4 zhun3] /not to allow/to forbid/to prohibit/'
        ]
        pinyin_jyutping.parser.parse_cedict_entries(lines, data)

        # pprint.pprint(data)
        self.assertEqual(len(data.character_map['谁']), 2)

        # check first character mapping
        character_mapping_1 = data.character_map['谁'][0]
        self.assertEqual(character_mapping_1.syllable, 
            PinyinSyllable(PinyinInitials.sh, PinyinFinals.ei, PinyinTones.tone_2),)
        self.assertEqual(character_mapping_1.occurences, 2)

        # check second character mapping
        character_mapping_2 = data.character_map['谁'][1]
        self.assertEqual(character_mapping_2.syllable, 
            PinyinSyllable(PinyinInitials.sh, PinyinFinals.ui, PinyinTones.tone_2),)
        self.assertEqual(character_mapping_2.occurences, 1)

        # check word
        self.assertEqual(len(data.word_map['不准']), 1)
        self.assertEqual(data.word_map['不准'][0].syllables,
        [
            PinyinSyllable(PinyinInitials.b, PinyinFinals.u, PinyinTones.tone_4),
            PinyinSyllable(PinyinInitials.zh, PinyinFinals.un, PinyinTones.tone_3)
        ]
        )

    def test_build_data_cedict_le(self):
        data = pinyin_jyutping.data.Data()
        # liao4 gets added to word map only, so when breaking down into characters, it gets ignored
        lines = [
            '瞭 了 [liao4] /unofficial variant of 瞭[liao4]/',
            '賣光了 卖光了 [mai4 guang1 le5] /to be sold out/to be out of stock/',
            '受得了 受得了 [shou4 de5 liao3] /to put up with/to endure/',
            '又來了 又来了 [you4 lai2 le5] /Here we go again./'
        ]
        pinyin_jyutping.parser.parse_cedict_entries(lines, data)

        pprint.pprint(data)
        self.assertEqual(len(data.character_map['了']), 3)
        self.assertEqual(len(data.word_map['了']), 3)

    def test_build_data_cedict_ordering(self):
        data = pinyin_jyutping.data.Data()
        lines = [
            '誰 谁 [shei2] /who/also pr. [shui2]/',
            '誰 谁 [shei2] /test 1/',
            '誰 谁 [shui2] /test 2/',
            '誰 谁 [shui2] /test 3/',
            '誰 谁 [shui2] /test 4/',
        ]
        pinyin_jyutping.parser.parse_cedict_entries(lines, data)

        # pprint.pprint(data)
        self.assertEqual(len(data.character_map['谁']), 2)

        # check first character mapping
        character_mapping_1 = data.character_map['谁'][0]
        self.assertEqual(character_mapping_1.syllable, 
            PinyinSyllable(PinyinInitials.sh, PinyinFinals.ui, PinyinTones.tone_2),)
        self.assertEqual(character_mapping_1.occurences, 3)

        # check second character mapping
        character_mapping_2 = data.character_map['谁'][1]
        self.assertEqual(character_mapping_2.syllable, 
            PinyinSyllable(PinyinInitials.sh, PinyinFinals.ei, PinyinTones.tone_2),)
        self.assertEqual(character_mapping_2.occurences, 2)


    @pytest.mark.skip(reason="a bit slow")
    def test_load_cedict(self):
        data = pinyin_jyutping.data.Data()
        filename = 'source_data/cedict_1_0_ts_utf-8_mdbg.txt'
        pinyin_jyutping.parser.parse_cedict(filename, data)

        self.assertIn('上周', data.simplified_map.word_map)
        self.assertEqual(len(data.simplified_map.word_map['上周']), 1)
        self.assertEqual(data.simplified_map.word_map['上周'][0].syllables,
            [ 
                PinyinSyllable(PinyinInitials.sh, PinyinFinals.ang, PinyinTones.tone_4),
                PinyinSyllable(PinyinInitials.zh, PinyinFinals.ou, PinyinTones.tone_1)
            ]
        )    

    def render_syllable_for_cedict(self, syllable):
        result = syllable.render_tone_number()
        result = result.replace('ü', 'u:')
        # if syllable.final == pinyin_jyutping.constants.PinyinFinals.er and \
        #     syllable.tone == pinyin_jyutping.constants.PinyinTones.tone_neutral:
        #     result = result.replace('er', 'r')
        return result

    def transform_pinyin_from_cedict(self, pinyin):
        if pinyin == 'r5':
            return 'er5'
        pinyin = pinyin.replace(' r5', ' er5')
        return pinyin

    @pytest.mark.skip(reason="skip")
    def test_verify_parse_output_pinyin(self):
        # pytest test_build_data.py  -k test_verify_parse_output_pinyin -s -rPP
        """parse all of cedict, and make sure we can faithfully output the pinyin"""
        filename = 'source_data/cedict_1_0_ts_utf-8_mdbg.txt'
        generator = pinyin_jyutping.parser.parse_cedict_file_generator(filename)
        error_count = 0
        processed_entries = 0
        for line in generator:
            traditional_chinese, simplified_chinese, pinyin, definition = pinyin_jyutping.parser.unpack_cedict_line(line)
            # should we skip this character ?
            skip = pinyin_jyutping.parser.cedict_ignore(traditional_chinese, simplified_chinese, pinyin)
            if not skip:
                syllables = pinyin_jyutping.parser.parse_pinyin_word(pinyin)
                pinyin_tone_numbers = ' '.join([self.render_syllable_for_cedict(x) for x in syllables])
                clean_pinyin = pinyin_jyutping.parser.clean_pinyin(pinyin)
                clean_pinyin = self.transform_pinyin_from_cedict(clean_pinyin)
                self.assertEqual(clean_pinyin, pinyin_tone_numbers, f'while parsing pinyin: {pinyin}')
                processed_entries += 1
        self.assertGreater(processed_entries, 97000)

    @pytest.mark.skip(reason="skip") 
    def test_verify_cedict_character_mapping(self):
        # pytest test_build_data.py  -k test_verify_cedict_character_mapping -s -rPP
        """parse all of cedict, and make sure we can faithfully output the pinyin"""
        filename = 'source_data/cedict_1_0_ts_utf-8_mdbg.txt'
        generator = pinyin_jyutping.parser.parse_cedict_file_generator(filename)
        data = pinyin_jyutping.data.Data()

        # analyze entries which contain this character only
        character_check = '拿'
        pinyin_jyutping.parser.DEBUG_WORD = character_check

        for line in generator:
            traditional_chinese, simplified_chinese, pinyin, definition = pinyin_jyutping.parser.unpack_cedict_line(line)
            # should we skip this character ?
            skip = pinyin_jyutping.parser.cedict_ignore(traditional_chinese, simplified_chinese, pinyin)
            if character_check not in simplified_chinese:
                skip = True
            if not skip:
                syllables = pinyin_jyutping.parser.parse_pinyin_word(pinyin)
                logger.warn(f'{simplified_chinese}: syllables: {syllables} pinyin: [{pinyin}]')
                pinyin_jyutping.parser.process_word(simplified_chinese, syllables, data)





if __name__ == '__main__':
    pass