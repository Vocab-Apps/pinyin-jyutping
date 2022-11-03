
class WordMapping():
    def __init__(self):
        self.syllables = None
        self.occurences = 0

class CharacterMapping():
    def __init__(self):
        self.syllable = None
        self.occurences = 0

class WordAndCharacterMaps():
    def __init__(self):
        self.character_map = {}
        self.word_map = {}

class Data():
    def __init__(self):
        self.simplified_map = WordAndCharacterMaps()
        self.traditonal_map = WordAndCharacterMaps()