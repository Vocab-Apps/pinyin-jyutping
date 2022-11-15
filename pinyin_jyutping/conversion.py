import jieba
import logging
import copy

logger = logging.getLogger(__file__)


def fill_pinyin_solution_for_characters(data, characters, current_solution, all_solutions):
    if len(characters) == 0:
        all_solutions.append(current_solution)
        return
    current_character = characters[0]    
    remaining_characters = characters[1:]
    entry = data.pinyin_map.get(current_character, None)
    if entry != None:
        for result in entry:
            new_solution = copy.copy(current_solution)
            new_solution.append(result.syllables[0])
            fill_pinyin_solution_for_characters(data, remaining_characters, new_solution, all_solutions)
    else:
        # implement pass through syllable here
        raise Exception('pass through syllable not implemented yet')

def get_pinyin_solutions_for_characters(data, word):
    all_solutions = []
    fill_pinyin_solution_for_characters(data, word, [], all_solutions)
    return all_solutions

def get_pinyin_solutions_for_word(data, word):
    entry = data.pinyin_map.get(word, None)
    if entry != None:
        return [mapping.syllables for mapping in entry]
    else:
        return get_pinyin_solutions_for_characters(data, word)

def get_pinyin_solutions(data, word_list):
    return [get_pinyin_solutions_for_word(data, word) for word in word_list]


def expand_solutions(data, word_list, current_solution, expanded_solution_list):
    if len(word_list) == 0:
        expanded_solution_list.append(current_solution)
        return

    current_word = word_list[0]
    remaining_words = word_list[1:]

    for alternative in current_word:
        new_solution = copy.copy(current_solution)
        new_solution.append(alternative)
        expand_solutions(data, remaining_words, new_solution, expanded_solution_list)


def expand_all_pinyin_solutions(data, word_list):
    expanded_solution_list = []
    solutions = get_pinyin_solutions(data, word_list)
    expand_solutions(data, solutions, [], expanded_solution_list)
    return expanded_solution_list


def render_word(word, tone_numbers, spaces): 
    join_syllables_character = ''
    if spaces:
        join_syllables_character = ' '        
    if tone_numbers:
        rendered_list = [syllable.render_tone_number() for syllable in word]
    else:
        rendered_list = [syllable.render_tone_mark() for syllable in word]
    return join_syllables_character.join(rendered_list)

def render_solution(solution, tone_numbers, spaces):
    return ' '.join([render_word(word, tone_numbers, spaces) for word in solution])

def render_all_pinyin_solutions(data, word_list, tone_numbers, spaces):
    expanded_solution_list = expand_all_pinyin_solutions(data, word_list)
    return [render_solution(solution, tone_numbers, spaces) for solution in expanded_solution_list]



# def render_all_pinyin_solutions(data, word_list):
#     solution_array = 

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
