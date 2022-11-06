
class WordMapping():
    def __init__(self, syllables):
        self.syllables = syllables
        self.occurences = 1

class CharacterMapping():
    def __init__(self, syllable):
        self.syllable = syllable
        self.occurences = 1

class Data():
    def __init__(self):
        self.character_map = {}
        self.word_map = {}

