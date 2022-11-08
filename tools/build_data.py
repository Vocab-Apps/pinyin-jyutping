import os
import sys
import pickle
import logging
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

logger = logging.getLogger(__file__)

import pinyin_jyutping.data
import pinyin_jyutping.parser
import pinyin_jyutping.constants

data = pinyin_jyutping.data.Data()

# ingest cedict data
filename = 'source_data/cedict_1_0_ts_utf-8_mdbg.txt'
pinyin_jyutping.parser.parse_cedict(filename, data)            

pickle_file_path = f'pinyin_jyutping/{pinyin_jyutping.constants.PICKLE_DATA_FILENAME}'
data_file = open(pickle_file_path, 'wb')
pickle.dump(data, data_file)
data_file.close()

logger.info(f'wrote {pickle_file_path}')