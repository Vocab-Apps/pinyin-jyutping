import jieba
import logging

logger = logging.getLogger(__file__)

# def process_pinyin_word(data, solutions, solution_id)

def process_remaining_pinyin(data, character_list, word_list, solution_list, solution, tone_numbers, spaces):
    logger.info(f'process_remaining_pinyin character_list: {character_list}, word_list: {word_list}')

    join_syllables_character = ''
    if spaces:
        join_syllables_character = ' '    

    if len(character_list) == 0 and len(word_list) == 0:
        solution_list.append(solution)
        return

    if len(character_list) > 0:
        first_character = character_list[0]
        remaining_characters = character_list[1:]
        if first_character in data.character_map:
            for entry in data.character_map[first_character]:
                if tone_numbers:
                    pinyin = entry.syllable.render_tone_number()
                else:
                    pinyin = entry.syllable.render_tone_mark()
                new_solution = solution + pinyin
                process_remaining_pinyin(data, remaining_characters, word_list, solution_list, new_solution, tone_numbers, spaces)
    elif len(word_list) > 0:
        first_word = word_list[0]
        remaining_words = word_list[1:]
        if first_word in data.word_map:
            for entry in data.word_map[first_word]:
                if tone_numbers:
                    pinyin = join_syllables_character.join([x.render_tone_number() for x in entry.syllables])
                else:
                    pinyin = join_syllables_character.join([x.render_tone_mark() for x in entry.syllables])
                new_solution = solution + pinyin
                process_remaining_pinyin(data, character_list, remaining_words, solution_list, new_solution, tone_numbers, spaces)
        else:
            # process as characters
            character_list = first_word
            process_remaining_pinyin(data, character_list, remaining_words, solution_list, solution, tone_numbers, spaces)


def convert_pinyin(data, text, tone_numbers, spaces):
    solution_list = []
    word_list = tokenize(text)
    process_remaining_pinyin(data, '', word_list, solution_list, '', tone_numbers, spaces)
    return solution_list


def tokenize(text):
    seg_list = jieba.cut(text)
    word_list = list(seg_list)
    return word_list
