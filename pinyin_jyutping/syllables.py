
class PinyinSyllable():
    def __init__(self, initial, final, tone):
        self.initial = initial
        self.final = final
        self.tone = tone

    def __eq__(self, other):
        if other == None:
            return False
        return self.initial == other.initial and \
               self.final == other.final and \
               self.tone == other.tone