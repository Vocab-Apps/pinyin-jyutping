import os
import pickle
import jieba
import logging
from . import constants
from . import conversion
from . import parser

logger = logging.getLogger(__file__)

class PinyinJyutping():
    def __init__(self):
        self.load_data()
        self.initialize_jieba()

    def load_data(self):
        module_dir = os.path.dirname(__file__)
        pickle_filepath = os.path.join(module_dir, constants.PICKLE_DATA_FILENAME)
        f = open(pickle_filepath, 'rb')
        self.data = pickle.load(f)
        f.close()

    def initialize_jieba(self):
        module_dir = os.path.dirname(__file__)
        jieba_big_dictionary_filename = os.path.join(module_dir, "dict.txt.big")
        jieba.set_dictionary(jieba_big_dictionary_filename)        

    def load_pinyin_corrections(self, corrections):
        for correction in corrections:
            try:
                chinese = correction['chinese']
                pinyin = correction['pinyin']
                parser.parse_pinyin_correction(chinese, pinyin, self.data)
            except Exception as e:
                logger.exception(e)

    def load_jyutping_corrections(self, corrections):
        for correction in corrections:
            try:
                chinese = correction['chinese']
                jyutping = correction['jyutping']
                parser.parse_jyutping_correction(chinese, jyutping, self.data)
            except Exception as e:
                logger.exception(e)                

    def pinyin(self, text, tone_numbers=False, spaces=False):
        return conversion.convert_pinyin_single_solution(self.data, text, tone_numbers, spaces)

    def jyutping(self, text, tone_numbers=False, spaces=False):
        return conversion.convert_jyutping_single_solution(self.data, text, tone_numbers, spaces)
    
    def pinyin_all_solutions(self, text, tone_numbers=False, spaces=False):
        return conversion.convert_pinyin_all_solutions(self.data, text, tone_numbers, spaces)

    def jyutping_all_solutions(self, text, tone_numbers=False, spaces=False):
        return conversion.convert_jyutping_all_solutions(self.data, text, tone_numbers, spaces)        
