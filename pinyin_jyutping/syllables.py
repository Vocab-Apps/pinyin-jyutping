
class PinyinSyllable():
    def __init__(self, initial, final, tone):
        self.initial = initial
        self.final = final
        self.tone = tone

    def render_tone_mark(self):
        return f'{self.initial.name}{self.final.name}'

    def render_tone_number(self):
        return f'{self.initial.name}{self.final.name}{self.tone.tone_number}'

    def __eq__(self, other):
        if other == None:
            return False
        return self.initial == other.initial and \
               self.final == other.final and \
               self.tone == other.tone