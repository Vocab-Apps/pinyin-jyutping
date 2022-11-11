import jieba


def convert_pinyin_words(data, word_list, tone_numbers, spaces):
    solutions = []
    result_words = []

    if len(word_list) == 0:
        return []

    first_word = word_list[0]
    remaining_words = word_list[1:]

    join_syllables_character = ''
    if spaces:
        join_syllables_character = ' '
    for word in word_list:
        if word in data.word_map:
            pinyin = join_syllables_character.join([x.render_tone_number() for x in data.word_map[word][0].syllables])
            result_words.append(pinyin)
        else:
            pinyin_components = []
            for character in word:
                if character in data.character_map:
                    pinyin_components.append(data.character_map[character][0].syllable.render_tone_number())
            result_words.append(join_syllables_character.join(pinyin_components))
                
    solutions.append(' '.join(result_words))
    return solutions


def convert_pinyin(data, text, tone_numbers, spaces):
    word_list = tokenize(text)
    return convert_pinyin_words(data, word_list, tone_numbers, spaces)


def tokenize(text):
    seg_list = jieba.cut(text)
    word_list = list(seg_list)
    return word_list
