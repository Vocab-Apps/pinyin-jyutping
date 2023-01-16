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

def parse_romanization(text, syllables_map, max_length):
    # look for initial
    original_text = text

    logger.debug(f'looking for pinyin syllable in {text}')
    # pprint.pprint(cache.PinyinFinalsMap)    
    for candidate_length in reversed(range(max_length + 1)):
        candidate = text[0:candidate_length]
        remaining_text = text[candidate_length:]
        # logger.debug(f'scanning for {candidate}, map size: {len(cache.PinyinFinalsMap)}')
        cache_hit = syllables_map.get(candidate, None)
        if cache_hit != None:
            return cache_hit, remaining_text
    raise errors.PinyinSyllableNotFound(f"couldn't find pinyin syllable: {text} [{original_text}]")


def parse_romanized_word(text, syllables_map, max_length):
    syllables = []
    while len(clean_romanization(text)) > 0:
        logger.debug(f'parsing pinyin word: {text}')
        # remove leading space
        text = clean_romanization(text)
        syllable, text = parse_romanization(text, syllables_map, max_length)
        logger.debug(f'parsed {syllable}, remaining text: {text}')
        syllables.append(syllable)
    return syllables

def parse_pinyin(text):
    return parse_romanized_word(text, cache.PinyinSyllablesMap, cache.PINYIN_SYLLABLE_MAX_LENGTH)

def parse_jyutping(text):
    return parse_romanized_word(text, cache.JyutpingSyllablesMap, cache.JYUTPING_SYLLABLE_MAX_LENGTH)

def clean_romanization(text):
    text = text.lower()
    text = text.lstrip()
    text = text.replace(',', '')
    text = text.replace('，', '')
    text = text.replace('、', '')
    text = text.replace('·', '')
    text = text.replace('？', ' ')
    text = text.replace('！', ' ')
    text = text.replace('。', ' ')
    text = text.replace('/', ' ')
    text = text.replace('...', ' ')
    text = text.replace('…', ' ')
    text = text.replace('.', '')
    text = text.replace('“', '')
    text = text.replace('”', '')
    text = text.replace('  ', ' ')    
    return text
 
def clean_chinese(text):
    text = text.strip()
    text = text.replace(',', '')
    text = text.replace('·', '')
    text = text.replace(' ', '')
    text = text.replace('，', '')
    return text    

# CEDICT parsing logic
# ====================

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

def parse_pinyin_correction(chinese, pinyin, data):
    chinese = clean_chinese(chinese)
    syllables = parse_pinyin(pinyin)
    process_word(chinese, syllables, data.pinyin_map, priority=True)

def parse_jyutping_correction(chinese, jyutping, data):
    chinese = clean_chinese(chinese)
    syllables = parse_jyutping(jyutping)
    process_word(chinese, syllables, data.jyutping_map, priority=True)

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
    return simplified_chinese, traditional_chinese, parse_pinyin(pinyin)

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

# CC-Canto parsing logic
# ======================

# this is a generator
def parse_cccanto_line_generator(filepath):
    with open(filepath, 'r', encoding="utf8") as filehandle:
        for line in filehandle:
            first_char = line[:1]
            if first_char != '#' and line != "and add boilerplate:\n":
                yield line

def parse_cccanto_definition_generator(filepath):
    for line in parse_cccanto_line_generator(filepath):
        logger.debug(f'parsing cedict line: {line}')
        m = re.match('(.+)\s\[([^\]]*)\]\s\{([^\]]*)\}\s\/([^\/]+)\/.*', line)
        if m == None:
            logger.error(f'could not parse line: {line}')
            continue
        traditional_simplified_chinese = m.group(1)
        pinyin = m.group(2)
        jyutping = m.group(3)
        definition = m.group(4)
        traditional_simplified_chinese = traditional_simplified_chinese.strip()
        # uneven length, because of the central space
        assert len(traditional_simplified_chinese) % 2 == 1, f'length: {len(traditional_simplified_chinese)}, [{traditional_simplified_chinese}]'
        half_length = int(len(traditional_simplified_chinese) / 2)
        traditional_chinese = clean_chinese(traditional_simplified_chinese[0:half_length])
        simplified_chinese = clean_chinese(traditional_simplified_chinese[half_length + 1:])
        yield {
            'simplified_chinese': simplified_chinese, 
            'traditional_chinese': traditional_chinese, 
            'pinyin':pinyin,
            'jyutping': jyutping
        }
        
def parse_cccedit_canto_readings_generator(filepath):
    for line in parse_cccanto_line_generator(filepath):
        m = re.match('(.+)\s\[([^\]]*)\]\s\{([^\]]*)\}.*', line)
        if m == None:
            logger.error(f'could not parse line: {line}')
            continue
        traditional_simplified_chinese = m.group(1)
        pinyin = m.group(2)
        jyutping = m.group(3)
        traditional_simplified_chinese = traditional_simplified_chinese.strip()
        # uneven length, because of the central space
        assert len(traditional_simplified_chinese) % 2 == 1, f'length: {len(traditional_simplified_chinese)}, [{traditional_simplified_chinese}]'
        half_length = int(len(traditional_simplified_chinese) / 2)
        traditional_chinese = clean_chinese(traditional_simplified_chinese[0:half_length])
        simplified_chinese = clean_chinese(traditional_simplified_chinese[half_length + 1:])
        yield {
            'simplified_chinese': simplified_chinese, 
            'traditional_chinese': traditional_chinese, 
            'pinyin':pinyin,
            'jyutping': jyutping
        }
    
def parse_jyutping_cccanto_definition_process_words(filepath, data):
    return parse_jyutping_process_words(parse_cccanto_definition_generator, filepath, data)    

def parse_jyutping_ccedit_canto_readings_process_words(filepath, data):
    return parse_jyutping_process_words(parse_cccedit_canto_readings_generator, filepath, data)

def parse_jyutping_process_words(generator, filepath, data):
    for entry in generator(filepath):
        jyutping = entry['jyutping']
        simplified = entry['simplified_chinese']
        traditional = entry['traditional_chinese']
        try:
            syllables = parse_jyutping(jyutping)
            # do some sanity checks on the length of syllables
            if (len(simplified) != len(syllables)) or (len(traditional) != len(syllables)):
                raise errors.PinyinParsingError(f'inconsistent lengths for jyutping {jyutping} simplified {simplified} traditional {traditional}')
            process_word(simplified, syllables, data.jyutping_map)
            process_word(traditional, syllables, data.jyutping_map)
        except errors.PinyinParsingError as e:
            logger.warning(e)            

def process_word(chinese, syllables, map, add_full_text=True, add_tokenized_words=True, add_characters=True, priority=False):
    # this is the sorting key
    def get_occurences(x):
        return x.occurences

    def add_word_mapping(chinese, word_map, syllables, priority):
        # if DEBUG_WORD != None:
        #     if chinese == DEBUG_WORD:
        #         logger.warn(f'adding word mapping: {chinese} syllable: {syllables}')

        if len(chinese) != len(syllables):
            raise Exception(f'{chinese} and {syllables}: inconsistent lengths')

        # insert into word map
        if chinese not in word_map:
            # will be initialized with occurences = 1
            # in priority mode, this is fine, it will be the only choice
            word_map[chinese] = [data.Mapping(syllables)]
        else:
            # does this pinyin exist already ?
            matching_entries = [x for x in word_map[chinese] if x.syllables == syllables]
            if len(matching_entries) == 1:
                # we already have this pinyin
                if priority:
                    matching_entries[0].occurences = constants.OCCURENCES_MAX
                else:
                    matching_entries[0].occurences += 1 
            elif len(matching_entries) == 0:
                # need to insert
                word_map[chinese].append(data.Mapping(syllables))
                if priority:
                    word_map[chinese][-1].occurences = constants.OCCURENCES_MAX
            else:
                pprint.pprint(word_map[chinese])
                raise Exception(f'found {len(matching_entries)} entries for [{chinese}], while processing {syllables}')
            word_map[chinese].sort(key=get_occurences, reverse=True)


    if add_full_text:
        # insert into word mapping
        add_word_mapping(chinese, map, syllables, priority)
    if add_tokenized_words:
        # add each word after jieba segmentation
        word_list = conversion.tokenize(chinese)
        remaining_syllables = syllables
        while len(word_list) > 0:
            chinese_word = word_list[0]
            word_list = word_list[1:]
            syllables_for_word = remaining_syllables[0:len(chinese_word)]
            remaining_syllables = remaining_syllables[len(chinese_word):]
            add_word_mapping(chinese_word, map, syllables_for_word, priority)
    if add_characters:
        # add each character
        if len(chinese) != len(syllables):
            raise Exception(f'found inconsistent lengths: {chinese}, {syllables}')
        for chinese_char, syllable in zip(chinese, syllables):
            add_word_mapping(chinese_char, map, [syllable], priority)


        
