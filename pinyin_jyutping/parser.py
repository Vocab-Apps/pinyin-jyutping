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
    raise errors.PinyinParsingError(f"couldn't find pinyin syllable: {text} [{original_text}]")


def parse_pinyin_word(text):
    syllables = []
    while len(text) > 0:
        logger.debug(f'parsing pinyin word: {text}')
        # remove leading space
        text = clean_pinyin(text)
        syllable, text = parse_pinyin(text)
        logger.debug(f'parsed {syllable}, remaining text: {text}')
        syllables.append(syllable)
    return syllables

def clean_pinyin(text):
    text = text.lstrip()
    text = text.replace(',', '')
    text = text.replace('·', '')
    text = text.replace('  ', ' ')
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
            simplified, traditional, syllables = parse_cedict_line(line)
            if (len(simplified) != len(syllables)) or (len(traditional) != len(syllables)):
                raise errors.PinyinParsingError(f'inconsistent lengths for line {line}')
            process_word(simplified, syllables, data)
            process_word(traditional, syllables, data)
        except errors.PinyinParsingError as e:
            logger.warning(e)


def unpack_cedict_line(line):
    logger.debug(f'parsing cedict line: {line}')
    m = re.match('([^\s]+)\s([^\s]+)\s\[([^\]]*)\]\s\/([^\/]+)\/.*', line)
    if m == None:
        logger.info(line)
    traditional_chinese = m.group(1)
    simplified_chinese = m.group(2)
    pinyin = m.group(3)
    definition = m.group(4)
    return traditional_chinese, simplified_chinese, pinyin, definition    

def parse_cedict_line(line):
    logger.debug(f'parsing cedict line: {line}')
    m = re.match('([^\s]+)\s([^\s]+)\s\[([^\]]*)\]\s\/([^\/]+)\/.*', line)
    if m == None:
        logger.info(line)
    traditional_chinese = m.group(1)
    simplified_chinese = m.group(2)
    pinyin = m.group(3)
    definition = m.group(4)        
    # parse the pinyin
    syllables = parse_pinyin_word(pinyin)
    return simplified_chinese, traditional_chinese, syllables

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

def process_word(chinese, syllables, map):
    # this is the sorting key
    def get_occurences(x):
        return x.occurences

    def add_character_mapping(chinese, character_map, syllable):
        if DEBUG_WORD != None:
            if chinese == DEBUG_WORD:
                logger.warn(f'adding character mapping: {chinese} syllable: {syllable}')

        # individual characters will always be lowercase
        if syllable.capital == True:
            syllable = copy.deepcopy(syllable)
            syllable.capital = False

        # insert into character map
        if chinese not in character_map:
            character_map[chinese] = [data.CharacterMapping(syllable)]
        else:
            # does this syllable exist already ?
            matching_entries = [x for x in character_map[chinese] if x.syllable == syllable]
            if len(matching_entries) == 1:
                # we already have this pinyin
                matching_entries[0].occurences += 1 
            elif len(matching_entries) == 0:
                # need to insert
                character_map[chinese].append(data.CharacterMapping(syllable))
            else:
                raise Exception(f'found {len(matching_entries)} for {chinese}')
            # sort by number of occurences, descending
            character_map[chinese].sort(key=get_occurences, reverse=True)

    def add_word_mapping(chinese, word_map, syllables):
        # if DEBUG_WORD != None:
        #     if chinese == DEBUG_WORD:
        #         logger.warn(f'adding word mapping: {chinese} syllable: {syllables}')

        if len(chinese) != len(syllables):
            raise Exception(f'{chinese} and {syllables}: inconsistent lengths')

        # insert into word map
        if chinese not in word_map:
            word_map[chinese] = [data.WordMapping(syllables)]
        else:
            # does this pinyin exist already ?
            matching_entries = [x for x in word_map[chinese] if x.syllables == syllables]
            if len(matching_entries) == 1:
                # we already have this pinyin
                matching_entries[0].occurences += 1 
            elif len(matching_entries) == 0:
                # need to insert
                word_map[chinese].append(data.WordMapping(syllables))
            else:
                pprint.pprint(word_map[chinese])
                raise Exception(f'found {len(matching_entries)} entries for [{chinese}], while processing {syllables}')
            word_map[chinese].sort(key=get_occurences, reverse=True)


    if len(chinese) == 1:
        # insert into character map
        add_character_mapping(chinese, map.character_map, syllables[0])
    else:
        # insert into word mapping
        add_word_mapping(chinese, map.word_map, syllables)
        # add each word after jieba segmentation
        word_list = conversion.tokenize(chinese)
        remaining_syllables = syllables
        while len(word_list) > 0:
            chinese_word = word_list[0]
            word_list = word_list[1:]
            syllables_for_word = remaining_syllables[0:len(chinese_word)]
            remaining_syllables = remaining_syllables[len(chinese_word):]
            add_word_mapping(chinese_word, map.word_map, syllables_for_word)
        # add each character
        for chinese_char, syllable in zip(chinese, syllables):
            add_character_mapping(chinese_char, map.character_map, syllable)


        
