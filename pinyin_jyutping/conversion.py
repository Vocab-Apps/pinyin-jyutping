import jieba
import logging

logger = logging.getLogger(__file__)

# def process_pinyin_word(data, solutions, solution_id)

def process_remaining_pinyin(data, character_list, word_list, solution_list, solution, tone_numbers, spaces):
    logger.debug(f'process_remaining_pinyin character_list: {character_list}, word_list: {word_list}')

    join_syllables_character = ''
    if spaces:
        join_syllables_character = ' '    

    leading_space = ''
    if len(solution ) > 0:
        leading_space = ' '

    if len(character_list) == 0 and len(word_list) == 0:
        # done with the recursion
        solution_list.append(solution)
        return

    if len(character_list) > 0:
        first_character = character_list[0]
        remaining_characters = character_list[1:]
        logger.debug(f'processing character_list: {character_list}, first_character: {first_character}')
        if first_character in data.pinyin_map:
            for entry in data.pinyin_map[first_character]:
                assert len(entry.syllables) == 1
                if tone_numbers:
                    pinyin = entry.syllables[0].render_tone_number()
                else:
                    pinyin = entry.syllables[0].render_tone_mark()
                new_solution = solution + pinyin
                process_remaining_pinyin(data, remaining_characters, word_list, solution_list, new_solution, tone_numbers, spaces)
        else:
            # leave character as is
            new_solution = solution + first_character
            process_remaining_pinyin(data, remaining_characters, word_list, solution_list, new_solution, tone_numbers, spaces)
    elif len(word_list) > 0:
        first_word = word_list[0]
        remaining_words = word_list[1:]
        logger.debug(f'processing word_list ({len(word_list)}) first_word: {first_word}')
        if first_word in data.pinyin_map:
            for entry in data.pinyin_map[first_word]:
                if tone_numbers:
                    pinyin = leading_space + join_syllables_character.join([x.render_tone_number() for x in entry.syllables])
                else:
                    pinyin = leading_space + join_syllables_character.join([x.render_tone_mark() for x in entry.syllables])
                new_solution = solution + pinyin
                process_remaining_pinyin(data, character_list, remaining_words, solution_list, new_solution, tone_numbers, spaces)
        else:
            # process as characters
            character_list = first_word
            new_solution = solution + leading_space
            process_remaining_pinyin(data, character_list, remaining_words, solution_list, new_solution, tone_numbers, spaces)


def convert_pinyin(data, text, tone_numbers, spaces):
    solution_list = []
    word_list = tokenize(text)
    process_remaining_pinyin(data, '', word_list, solution_list, '', tone_numbers, spaces)
    return solution_list


def tokenize(text):
    seg_list = jieba.cut(text)
    word_list = list(seg_list)
    return word_list
