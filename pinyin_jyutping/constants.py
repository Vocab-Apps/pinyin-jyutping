import enum

class PinyinInitials(enum.Enum):
    m = enum.auto()

PinyinInitialsMap = {initial.name:initial for initial in PinyinInitials}

class PinyinFinals(enum.Enum):
    a = ('ā', 'á', 'ǎ', 'à')
    o = ('ō', 'ó', 'ǒ', 'ò')

    def __init__(self, t1, t2, t3, t4):
        self.t1 = t1
        self.t2 = t2
        self.t3 = t3
        self.t4 = t4

PinyinFinalsMap = {final.name:final for final in PinyinFinals}

class PinyinTones(enum.Enum):
    tone_1 = (1)
    tone_2 = (2)
    tone_3 = (3)
    tone_4 = (4)
    tone_neutral = (5)

    def __init__(self, tone_number):
        self.tone_number = tone_number
