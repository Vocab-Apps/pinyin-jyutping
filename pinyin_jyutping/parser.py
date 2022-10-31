import logging

from . import constants
from . import syllables
from . import cache

logger = logging.getLogger(__file__)

def parse_pinyin(text):
    # look for initial
    # check first 2 letters
    first_2 = text[0:2]
    cache_hit = cache.PinyinInitialsMap.get(first_2, None)
    if cache_hit != None:
        remaining_text = text[2:]
        logger.debug(f'found initial: {first_2}')
        return parse_final_and_tone(cache_hit, remaining_text)
    first_1 = text[0:1]
    cache_hit = cache.PinyinInitialsMap.get(first_1, None)
    if cache_hit != None:
        remaining_text = text[1:]
        logger.debug(f'found initial {first_1}')
        return parse_final_and_tone(cache_hit, remaining_text)
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