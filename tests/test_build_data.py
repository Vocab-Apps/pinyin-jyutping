
import pickle
import unittest
import pytest
import pprint
import logging
import re
import sys
import os
import pdb


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

logger = logging.getLogger(__file__)

import pinyin_jyutping
import pinyin_jyutping.parser
import pinyin_jyutping.data
import pinyin_jyutping.logic
import pinyin_jyutping.constants

from pinyin_jyutping.syllables import PinyinSyllable
from pinyin_jyutping.constants import PinyinInitials, PinyinFinals, PinyinTones

ENABLE_FULL_CEDICT_PARSING_TESTS = os.environ.get('FULL_CEDICT_PARSING_TESTS', 'no') == 'yes'

class BuildTests(unittest.TestCase):

    # conversion tests
    # ================

    def build_data_from_input(self, input_data):
        data = pinyin_jyutping.data.Data()
        for entry in input_data:
            chinese, pinyin = entry
            syllables = pinyin_jyutping.parser.parse_pinyin(pinyin)
            pinyin_jyutping.parser.process_word(chinese, syllables, data.pinyin_map)
        return data

    def test_convert_pinyin_char(self):
        data = self.build_data_from_input([('没', 'mei2')])
        self.assertEqual(pinyin_jyutping.conversion.convert_pinyin_single_solution(data, '没', True, False), 'mei2')
        self.assertEqual(pinyin_jyutping.conversion.convert_pinyin_single_solution(data, '没', False, False), 'méi')

    def test_convert_pinyin_char_multiple_choice(self):
        data = self.build_data_from_input([
            ('没', 'mei2'),
            ('没', 'mei3'),
            ('没', 'mei2'),
        ])
        self.assertEqual(pinyin_jyutping.conversion.convert_pinyin_all_solutions(data, '没', True, False), [['mei2', 'mei3']])
        self.assertEqual(pinyin_jyutping.conversion.convert_pinyin_all_solutions(data, '没', False, False), [['méi', 'měi']])

    def test_convert_pinyin(self):
        input_data = [
            ('没有', 'mei2 you3')
        ]
        data = self.build_data_from_input(input_data)

        # no spaces    
        self.assertEqual(pinyin_jyutping.conversion.convert_pinyin_single_solution(data, '没有', True, False), 'mei2you3')
        # spaces
        self.assertEqual(pinyin_jyutping.conversion.convert_pinyin_single_solution(data, '没有', True, True), 'mei2 you3')

    def test_convert_pinyin_multiple_alternatives(self):
        input_data = [
            ('没有', 'mei2 you3'),
            ('没有', 'mei2 you3'),
            ('没有', 'mei2 you4'),
        ]
        data = self.build_data_from_input(input_data)

        # no spaces    
        self.assertEqual(pinyin_jyutping.conversion.convert_pinyin_all_solutions(data, '没有', True, False), [['mei2you3', 'mei2you4']])

    def test_convert_pinyin_words(self):
        input_data = [
            ('没有', 'mei2 you3'),
            ('什么', 'shen2 me5'),
        ]
        data = self.build_data_from_input(input_data)    
        self.assertEqual(pinyin_jyutping.conversion.convert_pinyin_single_solution(data, '没有什么', True, False), 'mei2you3 shen2me5')

    def test_convert_pinyin_sentences(self):
        input_data = [
            ('忘', 'wang4'),
            ('拿', 'na2'),
            ('一些', 'yīxiē'),
            ('东西', 'dōngxi'),
            ('了', 'le'),
        ]
        data = self.build_data_from_input(input_data)    
        self.assertEqual(pinyin_jyutping.conversion.convert_pinyin_single_solution(data, '忘拿一些东西了', True, False), 'wang4 na2 yi1xie1 dong1xi5 le5')

    def test_get_pinyin_solutions_for_word(self):
        input_data = [
            ('忘拿', 'wang4na2'),
            ('忘拿', 'wang4na3'),
        ]
        data = self.build_data_from_input(input_data)    
        expected_result = [
            [
                PinyinSyllable(PinyinInitials.empty, PinyinFinals.uang, PinyinTones.tone_4),
                PinyinSyllable(PinyinInitials.n, PinyinFinals.a, PinyinTones.tone_2),
            ],
            [
                PinyinSyllable(PinyinInitials.empty, PinyinFinals.uang, PinyinTones.tone_4),
                PinyinSyllable(PinyinInitials.n, PinyinFinals.a, PinyinTones.tone_3),
            ],            
        ]
        output = pinyin_jyutping.conversion.get_romanization_solutions_for_word(data.pinyin_map, '忘拿')
        print(output)
        print(type(output[0]))
        self.assertEqual(output,  expected_result)

    def test_get_pinyin_solutions_for_characters(self):
        input_data = [
            ('忘', 'wang4'),
            ('拿', 'na2'),
            ('拿', 'na3'),
        ]
        data = self.build_data_from_input(input_data)    
        expected_result = [
            [
                PinyinSyllable(PinyinInitials.empty, PinyinFinals.uang, PinyinTones.tone_4),
                PinyinSyllable(PinyinInitials.n, PinyinFinals.a, PinyinTones.tone_2),
            ],
            [
                PinyinSyllable(PinyinInitials.empty, PinyinFinals.uang, PinyinTones.tone_4),
                PinyinSyllable(PinyinInitials.n, PinyinFinals.a, PinyinTones.tone_3),
            ],            
        ]
        output = pinyin_jyutping.conversion.get_romanization_solutions_for_characters(data.pinyin_map, '忘拿')
        self.assertEqual(output,  expected_result)

    def test_get_pinyin_solutions(self):
        input_data = [
            ('忘', 'wang4'),
            ('拿', 'na2'),
            ('拿', 'na3'),
            ('东西', 'dong1 xi5')
        ]
        data = self.build_data_from_input(input_data)    
        expected_result = [
            [ # solutions for 忘
                [ # syllables
                    PinyinSyllable(PinyinInitials.empty, PinyinFinals.uang, PinyinTones.tone_4),
                ]

            ],

            [ # solutions for 拿
                [ # syllables
                    PinyinSyllable(PinyinInitials.n, PinyinFinals.a, PinyinTones.tone_2),
                ],
                [ # syllables
                    PinyinSyllable(PinyinInitials.n, PinyinFinals.a, PinyinTones.tone_3),
                ]                
            ],


            [ # solutions for 东西
                [ # syllables
                    PinyinSyllable(PinyinInitials.d, PinyinFinals.ong, PinyinTones.tone_1),
                    PinyinSyllable(PinyinInitials.x, PinyinFinals.i, PinyinTones.tone_neutral),
                ],
            ],
        ]

        output = pinyin_jyutping.conversion.get_romanization_solutions(data.pinyin_map, ['忘', '拿', '东西'])
        self.assertEqual(output,  expected_result)        

    def test_improve_tokenization(self):
        input_data = [
            ('投资', 'tou2 zi1'),
            ('银行', 'yin2 hang2'),

            ('个人', 'ge4 ren2'),
            ('所得税', 'suo3 de2 shui4')
        ]
        data = self.build_data_from_input(input_data)    
        
        word_list = ['投资银行']
        expected_result = ['投资', '银行']
        output = pinyin_jyutping.conversion.improve_tokenization(data.pinyin_map, word_list)
        self.assertEqual(output, expected_result)

        word_list = ['个人所得税']
        expected_result = ['个人', '所得税']
        output = pinyin_jyutping.conversion.improve_tokenization(data.pinyin_map, word_list)
        self.assertEqual(output, expected_result)        


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
        simplified, traditional, syllables = pinyin_jyutping.parser.parse_cedict_line_decode_pinyin(line)
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
        self.assertEqual(len(data.pinyin_map['谁']), 2)

        # check first character mapping
        character_mapping_1 = data.pinyin_map['谁'][0]
        self.assertEqual(character_mapping_1.syllables, 
            [PinyinSyllable(PinyinInitials.sh, PinyinFinals.ei, PinyinTones.tone_2)],)
        self.assertEqual(character_mapping_1.occurences, 4)

        # check second character mapping
        character_mapping_2 = data.pinyin_map['谁'][1]
        self.assertEqual(character_mapping_2.syllables, 
            [PinyinSyllable(PinyinInitials.sh, PinyinFinals.ui, PinyinTones.tone_2)],)
        self.assertEqual(character_mapping_2.occurences, 2)

        # check word
        self.assertEqual(len(data.pinyin_map['不准']), 1)
        self.assertEqual(data.pinyin_map['不准'][0].syllables,
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
        self.assertEqual(len(data.pinyin_map['了']), 3)
        self.assertEqual(len(data.pinyin_map['了']), 3)

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
        self.assertEqual(len(data.pinyin_map['谁']), 2)

        # check first character mapping
        character_mapping_1 = data.pinyin_map['谁'][0]
        self.assertEqual(character_mapping_1.syllables, 
            [PinyinSyllable(PinyinInitials.sh, PinyinFinals.ui, PinyinTones.tone_2)],)
        self.assertEqual(character_mapping_1.occurences, 9)

        # check second character mapping
        character_mapping_2 = data.pinyin_map['谁'][1]
        self.assertEqual(character_mapping_2.syllables, 
            [PinyinSyllable(PinyinInitials.sh, PinyinFinals.ei, PinyinTones.tone_2)],)
        self.assertEqual(character_mapping_2.occurences, 6)


    def test_user_corrections_existing(self):
        # variant 1: the correction is an existing variant, just push it up higher
        # ------------------------------------------------------------------------

        # first, build data using cedict
        data = pinyin_jyutping.data.Data()
        lines = [
            '誰 谁 [shei2] /who/also pr. [shui2]/',
            '誰 谁 [shei2] /test 1/',
            '誰 谁 [shui2] /test 2/',
        ]
        pinyin_jyutping.parser.parse_cedict_entries(lines, data)

        # the top result should be shei2
        character_mapping_1 = data.pinyin_map['谁'][0]
        self.assertEqual(character_mapping_1.syllables, 
            [PinyinSyllable(PinyinInitials.sh, PinyinFinals.ei, PinyinTones.tone_2)],)
        print(data.pinyin_map)

        # now, specify a correction
        # pdb.set_trace()
        pinyin_jyutping.parser.process_word('谁', 
            [PinyinSyllable(PinyinInitials.sh, PinyinFinals.ui, PinyinTones.tone_2)], data.pinyin_map, add_full_text=True, priority=True)

        # the top result should now be shui2
        character_mapping_first = data.pinyin_map['谁'][0]
        self.assertEqual(character_mapping_first.syllables, 
            [PinyinSyllable(PinyinInitials.sh, PinyinFinals.ui, PinyinTones.tone_2)],)
        self.assertEqual(character_mapping_first.occurences, pinyin_jyutping.constants.OCCURENCES_MAX)

    def test_user_corrections_new(self):
        # variant 2: the correction is a new variant
        # ------------------------------------------

        # first, build data using cedict
        data = pinyin_jyutping.data.Data()
        lines = [
            '誰 谁 [shei2] /who/also pr. [shui2]/',
            '誰 谁 [shei2] /test 1/',
            '誰 谁 [shui2] /test 2/',
        ]
        pinyin_jyutping.parser.parse_cedict_entries(lines, data)

        # now, specify a correction
        pinyin_jyutping.parser.process_word('谁', 
            [PinyinSyllable(PinyinInitials.sh, PinyinFinals.ei, PinyinTones.tone_4)], data.pinyin_map, add_full_text=True, priority=True)

        # the top result should now be shui2
        character_mapping_first = data.pinyin_map['谁'][0]
        self.assertEqual(character_mapping_first.syllables, 
            [PinyinSyllable(PinyinInitials.sh, PinyinFinals.ei, PinyinTones.tone_4)],)
        self.assertEqual(character_mapping_first.occurences, pinyin_jyutping.constants.OCCURENCES_MAX)


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

    @pytest.mark.skipif(ENABLE_FULL_CEDICT_PARSING_TESTS == False, reason="set FULL_CEDICT_PARSING_TESTS=yes")
    def test_verify_parse_output_pinyin(self):
        # FULL_CEDICT_PARSING_TESTS=yes pytest tests/test_build_data.py  -k test_verify_parse_output_pinyin -s -rPP
        """parse all of cedict, and make sure we can faithfully output the pinyin"""
        filename = 'source_data/cedict_1_0_ts_utf-8_mdbg.txt'
        generator = pinyin_jyutping.parser.parse_cedict_file_generator(filename)
        error_count = 0
        processed_entries = 0
        syllable_not_found_errors = 0
        for line in generator:
            traditional_chinese, simplified_chinese, pinyin = pinyin_jyutping.parser.parse_cedict_line(line)
            # should we skip this character ?
            skip = pinyin_jyutping.parser.cedict_ignore(traditional_chinese, simplified_chinese, pinyin)
            if not skip:
                try:
                    syllables = pinyin_jyutping.parser.parse_pinyin(pinyin)
                    pinyin_tone_numbers = ' '.join([self.render_syllable_for_cedict(x) for x in syllables])
                    clean_pinyin = pinyin_jyutping.parser.clean_romanization(pinyin)
                    clean_pinyin = self.transform_pinyin_from_cedict(clean_pinyin)
                    self.assertEqual(clean_pinyin, pinyin_tone_numbers, f'while parsing pinyin: {pinyin}')
                    processed_entries += 1
                except pinyin_jyutping.errors.PinyinSyllableNotFound as e:
                    syllable_not_found_errors += 1
                    logger.error(e)

        self.assertGreater(processed_entries, 118000)
        self.assertLess(syllable_not_found_errors, 5)

    @pytest.mark.skipif(ENABLE_FULL_CEDICT_PARSING_TESTS == False, reason="set FULL_CEDICT_PARSING_TESTS=yes")
    def test_verify_cedict_character_mapping(self):
        # pytest tests/test_build_data.py  -k test_verify_cedict_character_mapping -s -rPP
        """parse all of cedict, and make sure we can faithfully output the pinyin"""
        filename = 'source_data/cedict_1_0_ts_utf-8_mdbg.txt'
        generator = pinyin_jyutping.parser.parse_cedict_file_generator(filename)
        data = pinyin_jyutping.data.Data()

        # analyze entries which contain this character only
        character_check = '拿'
        pinyin_jyutping.parser.DEBUG_WORD = character_check

        for line in generator:
            traditional_chinese, simplified_chinese, pinyin = pinyin_jyutping.parser.parse_cedict_line(line)
            # should we skip this character ?
            skip = pinyin_jyutping.parser.cedict_ignore(traditional_chinese, simplified_chinese, pinyin)
            if character_check not in simplified_chinese:
                skip = True
            if not skip:
                syllables = pinyin_jyutping.parser.parse_pinyin(pinyin)
                logger.warn(f'{simplified_chinese}: syllables: {syllables} pinyin: [{pinyin}]')
                pinyin_jyutping.parser.process_word(simplified_chinese, syllables, data.pinyin_map)





if __name__ == '__main__':
    pass