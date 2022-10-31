import logging

from . import constants
from . import syllables
from . import cache

logger = logging.getLogger(__file__)

def parse_pinyin(text):
    # look for initial
    # check first 2 letters
    first_2 = text[0:2]
    remaining_text = text[2:]
    if first_2 in cache.PinyinInitialsMap:
        logger.debug(f'found initial: {first_2}')
        return parse_final_and_tone(constants.PinyinInitials[first_2], remaining_text)
    first_1 = text[0:1]
    remaining_text = text[1:]
    if first_1 in cache.PinyinInitialsMap:
        logger.debug(f'found initial {first_1}')
        return parse_final_and_tone(constants.PinyinInitials[first_1], remaining_text)
    raise Exception(f"couldn't find initial: {text}")

def parse_final_and_tone(initial, text):
    first_3 = text[0:3]
    first_2 = text[0:2]
    first_1 = text[0:1]
    for candidate in [first_3, first_2, first_1]:
        cache_hit = cache.PinyinFinalsMap.get(candidate, None)
        if cache_hit != None:
            final = cache_hit['final']
            tone = cache_hit['tone']
            return syllables.PinyinSyllable(initial, final, tone)
    raise Exception(f'could not find final: {text}')