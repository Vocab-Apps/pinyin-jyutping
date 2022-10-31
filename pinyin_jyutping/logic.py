from . import constants

def apply_tone_mark_on_vowel(pinyin_final, vowel, tone):
    tone_mark_vowel = constants.VowelToneMap[vowel][tone]
    return pinyin_final.name.replace(vowel, tone_mark_vowel)    

def vowel_for_tone_mark(pinyin_final, tone):
    # algorithm from https://en.wikipedia.org/wiki/Pinyin#Rules_for_placing_the_tone_mark    
    if pinyin_final.vowel_count == 1:
        location = pinyin_final.vowel_location
        return pinyin_final.name[location]
    elif pinyin_final.vowel_count == 2:
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

def apply_tone_mark(pinyin_final, tone):
    vowel = vowel_for_tone_mark(pinyin_final, tone)
    return apply_tone_mark_on_vowel(pinyin_final, vowel, tone)