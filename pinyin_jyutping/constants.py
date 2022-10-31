import enum

class PinyinInitials(enum.Enum):
    b = enum.auto()
    p = enum.auto()
    m = enum.auto()
    f = enum.auto()
    d = enum.auto()
    t = enum.auto()
    n = enum.auto()
    l = enum.auto()
    g = enum.auto()
    k = enum.auto()
    h = enum.auto()
    j = enum.auto()
    q = enum.auto()
    x = enum.auto()
    zh = enum.auto()
    ch = enum.auto()
    sh = enum.auto()
    r = enum.auto()
    z = enum.auto()
    c = enum.auto()
    s = enum.auto()
    y = enum.auto()
    w = enum.auto()

class PinyinFinals(enum.Enum):
    a  = (1, 0)
    o  = (1, 0)
    ie = (2, 0)

    def __init__(self, vowel_count, vowel_location):
        self.vowel_count = vowel_count
        self.vowel_location = vowel_location

class PinyinTones(enum.Enum):
    tone_1 = (1)
    tone_2 = (2)
    tone_3 = (3)
    tone_4 = (4)
    tone_neutral = (5)

    def __init__(self, tone_number):
        self.tone_number = tone_number

VowelToneMap = {
    'a': {
        PinyinTones.tone_1: 'ā', 
        PinyinTones.tone_2: 'á', 
        PinyinTones.tone_3: 'ǎ', 
        PinyinTones.tone_4: 'à',
        PinyinTones.tone_neutral: 'a'
    },
    'o': {
        PinyinTones.tone_1: 'ō',
        PinyinTones.tone_2: 'ó',
        PinyinTones.tone_3: 'ǒ',
        PinyinTones.tone_4: 'ò',
        PinyinTones.tone_neutral: 'o'
    },
    'e': {
        PinyinTones.tone_1: 'ē',
        PinyinTones.tone_2: 'é',
        PinyinTones.tone_3: 'ě',
        PinyinTones.tone_4: 'è',
        PinyinTones.tone_neutral: 'e'
    }
}


