
class Mapping():
    def __init__(self, syllables):
        self.syllables = syllables
        self.occurences = 1

    def __repr__(self):
        return f'{self.syllables} ({self.occurences})'

class Data():
    def __init__(self):
        self.pinyin_map = {}
        self.jyutping_map = {}

    def __str_(self):
        return f'{self.word_map}, {self.character_map}'