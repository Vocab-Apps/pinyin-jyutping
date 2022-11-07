import logging
from . import constants
from . import logic
from . import syllables

logger = logging.getLogger(__file__)

PINYIN_SYLLABLE_MAX_LENGTH=0

def build_pinyin_syllable_map():
    max_length = 0
    result_map = {}
    for initial in constants.PinyinInitials:
        for final in constants.PinyinFinals:
            for tone in constants.PinyinTones:
                for capital in [True, False]:
                    syllable = syllables.build_pinyin_syllable(initial, final, tone, capital)
                    tone_marks = syllable.render_tone_mark()
                    result_map[tone_marks] = syllable
                    tone_numbers = syllable.render_tone_number()
                    result_map[tone_numbers] = syllable

                    max_length = max(len(tone_numbers), max(len(tone_marks), max_length))

    return result_map, max_length

PinyinSyllablesMap, PINYIN_SYLLABLE_MAX_LENGTH = build_pinyin_syllable_map()