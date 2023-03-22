import enum

PICKLE_DATA_FILENAME='pinyin_jyutping.pkl'

# by default, we'll try to return all possible solutions. however the number of combinations
# quickly explodes with long inputs. if we exceed this number of words, just return the most likely solution.
MULTI_SOLUTION_MAX_WORD_COUNT = 50

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

class PinyinFinalGroup(enum.Enum):
    group_a = 1
    group_i = 2
    group_u = 3
    group_v = 4

# https://en.wikipedia.org/wiki/Pinyin_table
class PinyinFinals(enum.Enum):
    # group a finals
    a   =  ( 2 , PinyinFinalGroup.group_a )
    o   =  ( 3 , PinyinFinalGroup.group_a )
    e   =  ( 4 , PinyinFinalGroup.group_a )
    ai  =  ( 5 , PinyinFinalGroup.group_a )
    ei  =  ( 6 , PinyinFinalGroup.group_a )
    ao  =  ( 7 , PinyinFinalGroup.group_a )
    ou  =  ( 8 , PinyinFinalGroup.group_a )
    an  =  ( 9 , PinyinFinalGroup.group_a )
    en  =  (10 , PinyinFinalGroup.group_a )
    ang =  (11 , PinyinFinalGroup.group_a )
    eng =  (12 , PinyinFinalGroup.group_a )
    ong =  (13 , PinyinFinalGroup.group_a )
    er  =  (14 , PinyinFinalGroup.group_a, None, ['r'])
    # group i finals
    i   =  ( 1 , PinyinFinalGroup.group_i )    
    ia  =  (15 , PinyinFinalGroup.group_i )
    io  =  (16 , PinyinFinalGroup.group_i )
    ie  =  (17 , PinyinFinalGroup.group_i )
    iai =  (18 , PinyinFinalGroup.group_i )
    iao =  (19 , PinyinFinalGroup.group_i )
    iu  =  (20 , PinyinFinalGroup.group_i )
    ian =  (21 , PinyinFinalGroup.group_i )
    in_ =  (22 , PinyinFinalGroup.group_i, 'in')
    iang = (23 , PinyinFinalGroup.group_i )
    ing =  (24 , PinyinFinalGroup.group_i )
    iong = (25 , PinyinFinalGroup.group_i )
    # group u finals
    u   =  (26 , PinyinFinalGroup.group_u )
    ua  =  (27 , PinyinFinalGroup.group_u )
    uo  =  (28 , PinyinFinalGroup.group_u )
    uai =  (29 , PinyinFinalGroup.group_u )
    ui  =  (30 , PinyinFinalGroup.group_u )
    uan  = (31 , PinyinFinalGroup.group_u )
    un   = (32 , PinyinFinalGroup.group_u )
    uang = (33 , PinyinFinalGroup.group_u )
    ueng = (34 , PinyinFinalGroup.group_u )
    # group ü finals
    v   =  (35, PinyinFinalGroup.group_v, 'ü', ['u:']) # ü
    ve  =  (36, PinyinFinalGroup.group_v, 'üe', ['u:e'])
    van =  (37, PinyinFinalGroup.group_v, 'üan', ['u:an'])
    vn  =  (38, PinyinFinalGroup.group_v, 'ün')

    def __init__(self, value, final_group, override_final=None, variants=[]):
        self.val = value
        self.final_group = final_group
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

# https://en.wikipedia.org/wiki/Jyutping
# https://cantolounge.com/jyutping-chart/
# https://sla.talkbank.org/Jyutping/charts.html
class JyutpingInitials(enum.Enum):
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
    ng = 11
    h  = 12

    gw = 13
    kw = 14
    w  = 15

    z = 16
    c = 17
    s = 18
    j = 19

    empty = 20


class JyutpingFinals(enum.Enum):
    aa   = 1
    aai  = 2
    aau  = 3
    aam  = 4
    aan  = 6
    aang = 7
    aap  = 8
    aat  = 9
    aak  = 10
    a    = 11
    ai   = 12
    au   = 13
    am   = 14
    an   = 15
    ang  = 16
    ap   = 17
    at   = 18
    ak   = 19
    e    = 20
    ei   = 21
    eu   = 22
    em   = 23
    eng  = 24
    ep   = 25
    ek   = 26
    i    = 27
    iu   = 28
    im   = 29
    in_  = 30
    ing  = 31
    ip   = 32
    it   = 33
    ik   = 34
    o    = 35
    oi   = 36
    ou   = 37
    on   = 38
    ong  = 39
    ot   = 40
    ok   = 41
    u    = 42
    ui   = 43
    un   = 44
    ung  = 45
    ut   = 46
    uk   = 47
    eoi  = 48
    eon  = 49
    eot  = 50
    oe   = 51
    oeng = 52
    oet  = 53
    oek  = 54
    yu   = 55
    yun  = 56
    yut  = 57
    m    = 58
    ng   = 59
    et   = 60 # http://www.cantonese.sheik.co.uk/dictionary/characters/7763/
    
JYUTPING_SINGLE_FINALS = [
    JyutpingFinals.aa,
    JyutpingFinals.ai,
    JyutpingFinals.aai,
    JyutpingFinals.au,
    JyutpingFinals.aau,
    JyutpingFinals.o,
    JyutpingFinals.oi,
    JyutpingFinals.ou,
    JyutpingFinals.am,
    JyutpingFinals.aam,
    JyutpingFinals.aan,
    JyutpingFinals.ang,
    JyutpingFinals.aang,
    JyutpingFinals.on,
    JyutpingFinals.ong,
    JyutpingFinals.ung,
    JyutpingFinals.m,
    JyutpingFinals.ng,
    JyutpingFinals.ap,
    JyutpingFinals.aap,
    JyutpingFinals.aat,
    JyutpingFinals.ak,
    JyutpingFinals.aak,
    JyutpingFinals.ok,
    JyutpingFinals.uk,
]

class JyutpingTones(enum.Enum):
    tone_1 = (1)
    tone_2 = (2)
    tone_3 = (3)
    tone_4 = (4)
    tone_5 = (5)
    tone_6 = (6)

    def __init__(self, tone_number):
        self.tone_number = tone_number

JyutpingVowelToneMap = {
    'e':       {JyutpingTones.tone_1: 'ē',
                JyutpingTones.tone_2: 'é',
                JyutpingTones.tone_3: 'ê',
                JyutpingTones.tone_4: 'è',
                JyutpingTones.tone_5: 'ě',
                JyutpingTones.tone_6: 'e'},
    'a':     {JyutpingTones.tone_1: 'ā',
                JyutpingTones.tone_2: 'á',
                JyutpingTones.tone_3: 'â',
                JyutpingTones.tone_4: 'à',
                JyutpingTones.tone_5: 'ǎ',
                JyutpingTones.tone_6: 'a'},
    'i':     {JyutpingTones.tone_1: 'ī',
                JyutpingTones.tone_2: 'í',
                JyutpingTones.tone_3: 'î',
                JyutpingTones.tone_4: 'ì',
                JyutpingTones.tone_5: 'ǐ',
                JyutpingTones.tone_6: 'i'},
    'o':     {JyutpingTones.tone_1: 'ō',
                JyutpingTones.tone_2: 'ó',
                JyutpingTones.tone_3: 'ô',
                JyutpingTones.tone_4: 'ò',
                JyutpingTones.tone_5: 'ǒ',
                JyutpingTones.tone_6: 'o'},
    'u':     {JyutpingTones.tone_1: 'ū',
                JyutpingTones.tone_2: 'ú',
                JyutpingTones.tone_3: 'û',
                JyutpingTones.tone_4: 'ù',
                JyutpingTones.tone_5: 'ǔ',
                JyutpingTones.tone_6: 'u'}
    }

JYUTPING_ALL_VOWELS = list(JyutpingVowelToneMap.keys())


# when supplying user corrections, use this occurences value so that the result goes to the top
OCCURENCES_MAX = 10000