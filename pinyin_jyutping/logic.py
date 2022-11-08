from . import constants

def apply_tone_mark_on_vowel(pinyin_final, vowel, tone):
    tone_mark_vowel = constants.VowelToneMap[vowel][tone]
    return pinyin_final.final_text().replace(vowel, tone_mark_vowel)

def vowel_for_tone_mark(pinyin_final, tone):
    # algorithm from https://en.wikipedia.org/wiki/Pinyin#Rules_for_placing_the_tone_mark    
    if pinyin_final.vowel_count == 1:
        location = pinyin_final.vowel_location
        return pinyin_final.final_text()[location]
    elif pinyin_final.vowel_count > 1:
        vowel = 'a'
        if vowel in pinyin_final.name:
            return vowel
        vowel = 'e'
        if vowel in pinyin_final.name:
            return vowel
        vowel = 'o'
        if 'ou' in pinyin_final.name:
            return vowel
        else:
            # second vowel takes the tone mark
            location = pinyin_final.vowel_location + 1
            vowel = pinyin_final.name[location]
            return vowel
    raise Exception(f'could not find vowel for tone mark, final: {pinyin_final}')

def apply_tone_mark(pinyin_final, tone):
    vowel = vowel_for_tone_mark(pinyin_final, tone)
    return apply_tone_mark_on_vowel(pinyin_final, vowel, tone)


def get_initial_str(initial):
    result = ''
    if initial != constants.PinyinInitials.empty:
        result = initial.name
    return result

def get_final_str(initial, final):
    result = final.final_text()
    if initial == constants.PinyinInitials.empty:
        # apply replacements
        # from https://en.wikipedia.org/wiki/Pinyin_table
        if result[0] == 'i':
            result = 'y' + result[1:]
        elif result[0] == 'u':
            result = 'w' + result[1:]
        elif result[0] == 'ü':
            result = 'yu' + result[1:]

    return result

def render_tone_mark(initial, final, tone, capital):
    result = f'{get_initial_str(initial)}{apply_tone_mark(final, tone)}'
    if capital:
        result = result.capitalize()
    return result

def render_tone_number(initial, final, tone, capital, final_variant=None):
    final_str = get_final_str(initial, final)
    if final_variant != None:
        final_str = final_variant
    result = f'{get_initial_str(initial)}{final_str}{tone.tone_number}'
    if capital:
        result = result.capitalize()
    return result