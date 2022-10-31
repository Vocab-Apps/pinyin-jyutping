import logging

from . import constants
from . import syllables

logger = logging.getLogger(__file__)

def parse_pinyin(text):
    # look for initial
    # check first 2 letters
    first_2 = text[0:2]
    remaining_text = text[2:]
    if first_2 in constants.PinyinInitialsMap:
        logger.debug(f'found initial: {first_2}')
        return parse_final_and_tone(constants.PinyinInitials[first_2], remaining_text)
    first_1 = text[0:1]
    remaining_text = text[1:]
    if first_1 in constants.PinyinInitialsMap:
        logger.debug(f'found initial {first_1}')
        return parse_final_and_tone(constants.PinyinInitials[first_1], remaining_text)
    raise Exception(f"couldn't find initial: {text}")

def parse_final_and_tone(initial, text):
    for final in constants.PinyinFinals:
        logger.debug(f'scanning for final {final}, text: {text}')
        if text.startswith(final.t1):
            return syllables.PinyinSyllable(initial, final, constants.PinyinTones.tone_1)
        if text.startswith(final.t2):
            return syllables.PinyinSyllable(initial, final, constants.PinyinTones.tone_2)
        if text.startswith(final.t3):
            return syllables.PinyinSyllable(initial, final, constants.PinyinTones.tone_3)
        if text.startswith(final.t4):
            return syllables.PinyinSyllable(initial, final, constants.PinyinTones.tone_4)
    raise Exception(f'could not find final: {text}')