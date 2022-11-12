import pandas
import requests
import uuid
import os
import logging
import pprint

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__file__)

input_file = 'source_data/Mandarin_azure.txt'
columns = ['english', 'pinyin', 'chinese', 'sound', 'temp1', 'temp2', 'temp3', 'temp4']
data_df = pandas.read_csv(input_file, sep='\t', names=columns)
# data_df = pandas.read_csv(input_file, sep='\t')
print(data_df[['chinese', 'pinyin']])
data_df = data_df[['chinese', 'pinyin']]
data_df.to_json('source_data/anki_deck_1.json', orient='records')
