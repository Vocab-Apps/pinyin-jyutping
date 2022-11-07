import enum

PICKLE_DATA_FILENAME='pinyin_jyutping.pkl'
class PinyinInitials(enum.Enum):
    b  =  1
    p  =  2
    m  =  3
    f  =  4
    d  =  5
    t  =  6
    n  =  7
    l  =  8
    g  =  9
    k  = 10
    h  = 11
    j  = 12
    q  = 13
    x  = 14
    zh = 15
    ch = 16
    sh = 17
    r  = 18
    z  = 19
    c  = 20
    s  = 21
    y  = 22
    w  = 23
    empty = 24

class PinyinFinals(enum.Enum):
    a   = ( 1, 1, 0)
    o   = ( 2, 1, 0)
    e   = ( 3, 1, 0)
    i   = ( 4, 1, 0)
    u   = ( 5, 1, 0)
    v   = ( 6, 1, 0, 'ü') # ü
    ai  = ( 7, 2, 0)
    ei  = ( 8, 2, 0)
    ui  = ( 9, 2, 0)
    ao  = (10, 2, 0)
    ou  = (11, 2, 0)
    iu  = (12, 2, 0)
    ie  = (13, 2, 0)
    ve  = (14, 2, 0, 'üe')
    er  = (15, 1, 0)
    an  = (16, 1, 0)
    en  = (17, 1, 0)
    in_ = (18, 1, 0, 'in') # reserved keyword in python
    un  = (19, 1, 0)
    vn  = (20, 1, 0, 'ün')
    ang = (21, 1, 0)
    eng = (22, 1, 0)
    ing = (23, 1, 0)
    ong = (24, 1, 0)

    def __init__(self, value, vowel_count, vowel_location, override_final=None):
        self.val = value
        self.vowel_count = vowel_count
        self.vowel_location = vowel_location
        self.override_final = override_final

    def final_text(self):
        if self.override_final != None:
            return self.override_final
        return self.name

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
    },
    'i': {
        PinyinTones.tone_1: 'ī',
        PinyinTones.tone_2: 'í',
        PinyinTones.tone_3: 'ǐ',
        PinyinTones.tone_4: 'ì',
        PinyinTones.tone_neutral: 'i'
    },
    'u': {
        PinyinTones.tone_1: 'ū',
        PinyinTones.tone_2: 'ú',
        PinyinTones.tone_3: 'ǔ',
        PinyinTones.tone_4: 'ù',
        PinyinTones.tone_neutral: 'u'
    },
    'ü': {
        PinyinTones.tone_1: 'ǖ',
        PinyinTones.tone_2: 'ǘ',
        PinyinTones.tone_3: 'ǚ',
        PinyinTones.tone_4: 'ǜ',
        PinyinTones.tone_neutral: 'ü'
    },    

}


