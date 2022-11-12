
class WordMapping():
    def __init__(self, syllables):
        self.syllables = syllables
        self.occurences = 1

    def __repr__(self):
        return f'{self.syllables} ({self.occurences})'

class CharacterMapping():
    def __init__(self, syllable):
        self.syllable = syllable
        self.occurences = 1

class Data():
    def __init__(self):
        self.character_map = {}
        self.word_map = {}

    def __str_(self):
        return f'{self.word_map}, {self.character_map}'