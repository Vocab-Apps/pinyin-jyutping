import logging
import pprint
import re
import copy

from . import constants
from . import syllables
from . import cache
from . import errors
from . import data
from . import conversion

logger = logging.getLogger(__file__)

DEBUG_WORD = None

def parse_pinyin(text):
    # look for initial
    original_text = text

    logger.debug(f'looking for pinyin syllable in {text}')
    # pprint.pprint(cache.PinyinFinalsMap)    
    for candidate_length in reversed(range(cache.PINYIN_SYLLABLE_MAX_LENGTH + 1)):
        candidate = text[0:candidate_length]
        remaining_text = text[candidate_length:]
        # logger.debug(f'scanning for {candidate}, map size: {len(cache.PinyinFinalsMap)}')
        cache_hit = cache.PinyinSyllablesMap.get(candidate, None)
        if cache_hit != None:
            return cache_hit, remaining_text
    raise errors.PinyinSyllableNotFound(f"couldn't find pinyin syllable: {text} [{original_text}]")


def parse_pinyin_word(text):
    syllables = []
    while len(clean_pinyin(text)) > 0:
        logger.debug(f'parsing pinyin word: {text}')
        # remove leading space
        text = clean_pinyin(text)
        syllable, text = parse_pinyin(text)
        logger.debug(f'parsed {syllable}, remaining text: {text}')
        syllables.append(syllable)
    return syllables

def clean_pinyin(text):
    text = text.lower()
    text = text.lstrip()
    text = text.replace(',', '')
    text = text.replace('，', '')
    text = text.replace('·', '')
    text = text.replace('  ', ' ')
    text = text.replace('？', ' ')
    text = text.replace('。', ' ')
    text = text.replace('/', ' ')
    text = text.replace('...', ' ')
    text = text.replace('…', ' ')
    return text
 
def clean_chinese(text):
    text = text.strip()
    text = text.replace(',', '')
    text = text.replace('·', '')
    text = text.replace(' ', '')
    text = text.replace('，', '')
    return text    

def parse_cedict(filepath, data):
    generator = parse_cedict_file_generator(filepath)
    parse_cedict_entries(generator, data)

# this is a generator
def parse_cedict_file_generator(filepath):
    simplified_word_map = {}
    traditional_word_map = {}
    with open(filepath, 'r', encoding="utf8") as filehandle:
        for line in filehandle:
            first_char = line[:1]
            if first_char != '#' and line != "and add boilerplate:\n":
                yield line

def parse_cedict_entries(generator, data):
    for line in generator:
        try:
            simplified, traditional, syllables = parse_cedict_line_decode_pinyin(line)
            if (len(simplified) != len(syllables)) or (len(traditional) != len(syllables)):
                raise errors.PinyinParsingError(f'inconsistent lengths for line {line}')
            process_word(simplified, syllables, data.pinyin_map)
            process_word(traditional, syllables, data.pinyin_map)
        except errors.PinyinParsingError as e:
            logger.warning(e)


# returns raw pinyin text
def parse_cedict_line(line):
    logger.debug(f'parsing cedict line: {line}')
    m = re.match('(.+)\s\[([^\]]*)\]\s\/([^\/]+)\/.*', line)
    if m == None:
        logger.info(line)
    traditional_simplified_chinese = m.group(1)
    pinyin = m.group(2)
    definition = m.group(3)
    traditional_simplified_chinese = traditional_simplified_chinese.strip()
    # uneven length, because of the central space
    assert len(traditional_simplified_chinese) % 2 == 1, f'length: {len(traditional_simplified_chinese)}, [{traditional_simplified_chinese}]'
    half_length = int(len(traditional_simplified_chinese) / 2)
    traditional_chinese = clean_chinese(traditional_simplified_chinese[0:half_length])
    simplified_chinese = clean_chinese(traditional_simplified_chinese[half_length + 1:])
    return simplified_chinese, traditional_chinese, pinyin

# returns parsed pinyin
def parse_cedict_line_decode_pinyin(line):
    simplified_chinese, traditional_chinese, pinyin = parse_cedict_line(line)
    return simplified_chinese, traditional_chinese, parse_pinyin_word(pinyin)

def cedict_ignore(traditional_chinese, simplified_chinese, pinyin):
    if re.match('.*[A-Za-z].*', simplified_chinese) != None:
        return True                                
    if 'xx' in pinyin:
        return True
    if 'm2' in pinyin:
        return True        
    if 'm4' in pinyin:
        return True                
    return False

def process_word(chinese, syllables, map, add_full_text=True, add_tokenized_words=True, add_characters=True):
    # this is the sorting key
    def get_occurences(x):
        return x.occurences

    def add_word_mapping(chinese, word_map, syllables):
        # if DEBUG_WORD != None:
        #     if chinese == DEBUG_WORD:
        #         logger.warn(f'adding word mapping: {chinese} syllable: {syllables}')

        if len(chinese) != len(syllables):
            raise Exception(f'{chinese} and {syllables}: inconsistent lengths')

        # insert into word map
        if chinese not in word_map:
            word_map[chinese] = [data.Mapping(syllables)]
        else:
            # does this pinyin exist already ?
            matching_entries = [x for x in word_map[chinese] if x.syllables == syllables]
            if len(matching_entries) == 1:
                # we already have this pinyin
                matching_entries[0].occurences += 1 
            elif len(matching_entries) == 0:
                # need to insert
                word_map[chinese].append(data.Mapping(syllables))
            else:
                pprint.pprint(word_map[chinese])
                raise Exception(f'found {len(matching_entries)} entries for [{chinese}], while processing {syllables}')
            word_map[chinese].sort(key=get_occurences, reverse=True)


    if add_full_text:
        # insert into word mapping
        add_word_mapping(chinese, map, syllables)
    if add_tokenized_words:
        # add each word after jieba segmentation
        word_list = conversion.tokenize(chinese)
        remaining_syllables = syllables
        while len(word_list) > 0:
            chinese_word = word_list[0]
            word_list = word_list[1:]
            syllables_for_word = remaining_syllables[0:len(chinese_word)]
            remaining_syllables = remaining_syllables[len(chinese_word):]
            add_word_mapping(chinese_word, map, syllables_for_word)
    if add_characters:
        # add each character
        if len(chinese) != len(syllables):
            raise Exception(f'found inconsistent lengths: {chinese}, {syllables}')
        for chinese_char, syllable in zip(chinese, syllables):
            add_word_mapping(chinese_char, map, [syllable])


        
