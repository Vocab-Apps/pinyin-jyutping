import logging
from . import constants
from . import logic

logger = logging.getLogger(__file__)

# populate initials map
PinyinInitialsMap = {initial.name:initial for initial in constants.PinyinInitials}

def build_pinyin_finals_map():
    PinyinFinalsMap = {}
    for final in constants.PinyinFinals:
        for tone in constants.PinyinTones:
            with_tone_mark = logic.apply_tone_mark(final, tone)
            logger.debug(f'populating PinyinFinalsMap: {with_tone_mark}')
            PinyinFinalsMap[with_tone_mark] = {
                'final': final,
                'tone': tone
            }
            with_tone_number = f'{final.name}{tone.tone_number}'
            PinyinFinalsMap[with_tone_number] = {
                'final': final,
                'tone': tone
            }    
    return PinyinFinalsMap

# populate finals map
PinyinFinalsMap = build_pinyin_finals_map()
