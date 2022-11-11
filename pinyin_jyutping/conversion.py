import jieba
import logging

logger = logging.getLogger(__file__)

# def process_pinyin_word(data, solutions, solution_id)

def process_remaining_pinyin(data, character_list, word_list, solution_list, solution):
    logger.info(f'process_remaining_pinyin character_list: {character_list}, word_list: {word_list}')

    join_syllables_character = ''

    if len(character_list) == 0 and len(word_list) == 0:
        solution_list.append(solution)
        return

    if len(character_list) > 0:
        first_character = character_list[0]
        remaining_characters = character_list[1:]
        if first_character in data.character_map:
            for entry in data.character_map[first_character]:
                pinyin = entry.syllable.render_tone_number()
                new_solution = solution + pinyin
                process_remaining_pinyin(data, remaining_characters, word_list, solution_list, new_solution)
    elif len(word_list) > 0:
        first_word = word_list[0]
        remaining_words = word_list[1:]
        if first_word in data.word_map:
            for entry in data.word_map[first_word]:
                pinyin = join_syllables_character.join([x.render_tone_number() for x in entry.syllables])
                new_solution = solution + pinyin
                process_remaining_pinyin(data, character_list, remaining_words, solution_list, new_solution)
        else:
            # process as characters
            character_list = first_word
            process_remaining_pinyin(data, character_list, remaining_words, solution_list, solution)


def convert_pinyin_words(data, word_list, solution_list, tone_numbers, spaces):
    solutions = []
    result_words = []

    if len(word_list) == 0:
        return []

    first_word = word_list[0]
    remaining_words = word_list[1:]

    # if first_word in data.word_map:


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
    solution_list = []
    word_list = tokenize(text)
    process_remaining_pinyin(data, '', word_list, solution_list, '')
    return solution_list


def tokenize(text):
    seg_list = jieba.cut(text)
    word_list = list(seg_list)
    return word_list
