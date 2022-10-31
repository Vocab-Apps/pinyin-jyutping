from . import constants
from . import logic

# populate initials map
PinyinInitialsMap = {initial.name:initial for initial in constants.PinyinInitials}

# populate finals map
PinyinFinalsMap = {}
for final in constants.PinyinFinals:
    for tone in constants.PinyinTones:
        with_tone_mark = logic.apply_tone_mark(final, tone)
        PinyinFinalsMap[with_tone_mark] = {
            'final': final,
            'tone': tone
        }
        with_tone_number = f'{final.name}{tone.tone_number}'
        PinyinFinalsMap[with_tone_number] = {
            'final': final,
            'tone': tone
        }