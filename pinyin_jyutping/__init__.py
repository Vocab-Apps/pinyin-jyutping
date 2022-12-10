import os
import pickle
import jieba
from . import constants
from . import conversion
from . import parser

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

    def load_corrections(self, corrections):
        for correction in corrections:
            chinese = correction['chinese']
            pinyin = correction['pinyin']
            parser.parse_correction(chinese, pinyin, self.data)

    def pinyin(self, text, tone_numbers=False, spaces=False):
        return conversion.convert_pinyin(self.data, text, tone_numbers, spaces)

    def jyutping(self, text, tone_numbers=False, spaces=False):
        pass