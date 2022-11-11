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
    empty = 23

# https://en.wikipedia.org/wiki/Pinyin_table
class PinyinFinals(enum.Enum):
    # group a finals
    i   =  ( 1 )
    a   =  ( 2 )
    o   =  ( 3 )
    e   =  ( 4 )
    ai  =  ( 5 )
    ei  =  ( 6 )
    ao  =  ( 7 )
    ou  =  ( 8 )
    an  =  ( 9 )
    en  =  (10 )
    ang =  (11 )
    eng =  (12 )
    ong =  (13 )
    er  =  (14 , None, ['r'])
    # group i finals
    ia  =  (15 )
    io  =  (16 )
    ie  =  (17 )
    iai =  (18 )
    iao =  (19 )
    iu  =  (20 )
    ian =  (21 )
    in_ =  (22 , 'in')
    iang = (23 )
    ing =  (24 )
    iong = (25 )
    # group u finals
    u   =  (26 )
    ua  =  (27 )
    uo  =  (28 )
    uai =  (29 )
    ui  =  (30 )
    uan  = (31 )
    un   = (32 )
    uang = (33 )
    ueng = (34 )
    # group ü finals
    v   =  (35, 'ü', ['u:']) # ü
    ve  =  (36, 'üe', ['u:e'])
    van =  (37, 'üan', ['u:an'])
    vn  =  (38, 'ün')

    def __init__(self, value, override_final=None, variants=[]):
        self.val = value
        self.override_final = override_final
        self.variants = variants

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


ALL_VOWELS = list(VowelToneMap.keys()) + ['y']