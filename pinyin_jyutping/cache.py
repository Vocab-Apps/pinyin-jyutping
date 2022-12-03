import logging
from . import constants
from . import logic
from . import syllables

logger = logging.getLogger(__file__)

PINYIN_SYLLABLE_MAX_LENGTH=0

def all_syllables_generator():
    for initial in constants.PinyinInitials:
        for final in constants.PinyinFinals:
            if logic.valid_combination(initial, final):
                for tone in constants.PinyinTones:
                    syllable = syllables.build_pinyin_syllable(initial, final, tone)
                    tone_marks = syllable.render_tone_mark()
                    yield {
                        'syllable': syllable,
                        'pinyin': tone_marks
                    }
                    tone_numbers = syllable.render_tone_number()
                    yield {
                        'syllable': syllable,
                        'pinyin': tone_numbers
                    }
                    # are there any variants on the final ?
                    for final_variant in final.variants:
                        tone_numbers = syllable.render_tone_number(final_variant=final_variant)
                        yield {
                            'syllable': syllable,
                            'pinyin': tone_numbers
                        }                        



def build_pinyin_syllable_map():
    max_length = 0
    result_map = {}
    for entry in all_syllables_generator():    

        syllable = entry['syllable']
        pinyin = entry['pinyin']
        result_map[pinyin] = syllable

        max_length = max(len(pinyin),  max_length)

    return result_map, max_length

PinyinSyllablesMap, PINYIN_SYLLABLE_MAX_LENGTH = build_pinyin_syllable_map()