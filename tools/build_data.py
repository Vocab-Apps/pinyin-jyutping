import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import pinyin_jyutping.data
import pinyin_jyutping.parser

data = pinyin_jyutping.data.Data()

# ingest cedict data
filename = 'source_data/cedict_1_0_ts_utf-8_mdbg.txt'
pinyin_jyutping.parser.parse_cedict(filename, data)            



