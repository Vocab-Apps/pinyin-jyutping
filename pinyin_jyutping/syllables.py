from . import logic
from . import constants
import functools


class PinyinSyllable():
    def __init__(self, initial, final, tone):
        self.initial = initial
        self.final = final
        self.tone = tone

    def get_initial_str(self):
        result = ''
        if self.initial != constants.PinyinInitials.empty:
            result = self.initial.name
        return result

    def render_tone_mark(self):
        return logic.render_tone_mark(self.initial, self.final, self.tone)

    def render_tone_number(self, final_variant=None):
        return logic.render_tone_number(self.initial, self.final, self.tone, final_variant=final_variant)

    def __repr__(self):
        return f'{self.initial.name}-{self.final.name}-{self.tone.tone_number}'

    def __str__(self):
        return self.render_tone_number()

    def __eq__(self, other):
        if other == None:
            return False
        return self.initial == other.initial and \
               self.final == other.final and \
               self.tone == other.tone


# for characters we don't recognize, just pass them through
class PassThroughSyllable():
    def __init__(self, character):
        self.character = character
        self.tone = None

    def render_tone_mark(self):
        return self.character

    def render_tone_number(self):
        return self.character


@functools.lru_cache(maxsize=None)
def build_pinyin_syllable(initial, final, tone):
    return PinyinSyllable(initial, final, tone)

class JyutpingSyllable():
    def __init__(self, initial, final, tone):
        self.initial = initial
        self.final = final
        self.tone = tone

    def render_tone_mark(self):
        return logic.jyutping_render_tone_mark(self.initial, self.final, self.tone)

    def render_tone_number(self):
        return logic.jyutping_render_tone_number(self.initial, self.final, self.tone)

    def __repr__(self):
        return f'{self.initial.name}-{self.final.name}-{self.tone.tone_number}'

    def __str__(self):
        return self.render_tone_number()

    def __eq__(self, other):
        if other == None:
            return False
        return self.initial == other.initial and \
               self.final == other.final and \
               self.tone == other.tone

@functools.lru_cache(maxsize=None)
def build_jyutping_syllable(initial, final, tone):
    return JyutpingSyllable(initial, final, tone)