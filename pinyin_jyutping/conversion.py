import jieba
import logging
import copy
import pprint
from . import syllables
from . import logic
from . import constants

logger = logging.getLogger(__file__)


def fill_romanization_solution_for_characters(word_map, characters, current_solution, all_solutions):
    if len(characters) == 0:
        all_solutions.append(current_solution)
        return
    current_character = characters[0]    
    remaining_characters = characters[1:]
    entry = word_map.get(current_character, None)
    if entry != None:
        for result in entry:
            new_solution = copy.copy(current_solution)
            new_solution.append(result.syllables[0])
            fill_romanization_solution_for_characters(word_map, remaining_characters, new_solution, all_solutions)
    else:
        # implement pass through syllable here
        syllable = syllables.PassThroughSyllable(current_character)
        new_solution = copy.copy(current_solution)
        new_solution.append(syllable)
        fill_romanization_solution_for_characters(word_map, remaining_characters, new_solution, all_solutions)        

def get_romanization_solutions_for_characters(word_map, word):
    all_solutions = []
    fill_romanization_solution_for_characters(word_map, word, [], all_solutions)
    return all_solutions

def get_romanization_solutions_for_word(word_map, word):
    entry = word_map.get(word, None)
    if entry != None:
        logger.debug(f'located {word} as word')
        return [mapping.syllables for mapping in entry]
    else:
        logger.debug(f'breaking down {word} into characters')
        return get_romanization_solutions_for_characters(word_map, word)

def get_romanization_solutions(word_map, word_list):
    return [get_romanization_solutions_for_word(word_map, word) for word in word_list]

def render_word(word, tone_numbers, spaces): 
    join_syllables_character = ''
    if spaces:
        join_syllables_character = ' '        
    if tone_numbers:
        rendered_list = [syllable.render_tone_number() for syllable in word]
    else:
        rendered_list = [syllable.render_tone_mark() for syllable in word]
    return join_syllables_character.join(rendered_list)

def solutions_array_for_word(word_map, word):
    entry = word_map.get(word, None)
    if entry != None:
        logger.debug(f'located {word} as word')
        return [mapping.syllables for mapping in entry]
    else:
        logger.debug(f'breaking down {word} into characters')
        return get_romanization_solutions_for_characters(word_map, word)    

def render_solutions_array(solutions, tone_numbers, spaces):
    return [render_word(word, tone_numbers, spaces) for word in solutions]

def render_all_romanization_solutions(word_map, word_list, tone_numbers, spaces):
    # first, build array of arrays
    solutions_array = [solutions_array_for_word(word_map, word) for word in word_list]

    # apply pinyin tone change rules
    logic.apply_pinyin_tone_change(word_list, solutions_array)
    
    # now, render everything to the proper romanization
    rendered_solution = [render_solutions_array(solutions, tone_numbers, spaces) for solutions in solutions_array]

    return rendered_solution


def tokenize_to_word_list(word_map, text):
    word_list = tokenize(text)
    word_list = improve_tokenization(word_map, word_list)
    return word_list

def convert_to_romanization(word_map, text, tone_numbers, spaces):
    solution_list = []
    word_list = tokenize_to_word_list(word_map, text)
    solutions = render_all_romanization_solutions(word_map, word_list, tone_numbers, spaces)
    return {
        'word_list': word_list, 
        'solutions': solutions
    }

def convert_single_solution(word_map, text, tone_numbers, spaces):
    # first, get all solutions
    data = convert_to_romanization(word_map, text, tone_numbers, spaces)
    all_solutions = data['solutions']
    # just assemble the most probable solution for each word
    logger.debug(f'convert_single_solution, all_solutions: {pprint.pformat(all_solutions)}')
    return ' '.join(word_solutions[0] for word_solutions in all_solutions)

def convert_pinyin_single_solution(data, text, tone_numbers, spaces):
    word_map = data.pinyin_map
    return convert_single_solution(word_map, text, tone_numbers, spaces)

def convert_jyutping_single_solution(data, text, tone_numbers, spaces):
    word_map = data.jyutping_map
    return convert_single_solution(word_map, text, tone_numbers, spaces)

def convert_pinyin_all_solutions(data, text, tone_numbers, spaces):
    return convert_to_romanization(data.pinyin_map, text, tone_numbers, spaces)

def convert_jyutping_all_solutions(data, text, tone_numbers, spaces):
    return convert_to_romanization(data.jyutping_map, text, tone_numbers, spaces)

def tokenize(text):
    seg_list = jieba.cut(text)
    word_list = list(seg_list)
    return word_list

def improve_tokenization(word_map, word_list):
    # sometimes jieba will not tokenize certain words like 投资银行, however the character-by-character
    # pinyin conversion renders the last character as xing2. a second pass to try to further break down
    # if the word is not found in the pinyin dictionary gives a better chance to find a good match.
    # for example with 投资银行, breaking down as 投资, 银行 is better

    iterations = 0

    final_word_list = []
    for word in word_list:
        if len(word) == 1 or word in word_map:
            final_word_list.append(word)
        else:
            logger.debug(f'attempting improved tokenization for {word}')
            word_breakdown = []
            word_remaining_chars = word
            found_larger_matches = 0
            continue_iteration = True
            while continue_iteration:
                iterations += 1
                assert iterations < 1000, f'infinite loop while running improve_tokenization for {word_list}'

                logger.debug(f'word_remaining_chars: [{word_remaining_chars}]')
                # try to identify sub-words which are present in the map
                found_matches = False
                for i in range(len(word_remaining_chars) - 1, 1, -1):
                    logger.debug(f'looking for word of length {i}')
                    sub_word = word_remaining_chars[0:i]
                    if sub_word in word_map:
                        logger.debug(f'found match for {sub_word}')
                        found_matches = True
                        word_breakdown.append(sub_word) 
                        word_remaining_chars = word_remaining_chars[i:]
                        found_larger_matches += 1
                        break
                logger.debug(f'found_matches: {found_matches}')
                if found_matches == False:
                    continue_iteration = False
                #continue_iteration = 
                if len(word_remaining_chars) <= 2:
                    continue_iteration = False

            if len(word_remaining_chars) > 0:
                word_breakdown.append(word_remaining_chars)
            
            # did we find larger matches ?
            if found_larger_matches > 0:
                # then use the new breakdown
                final_word_list.extend(word_breakdown)
            else:
                # use original word
                final_word_list.append(word)
                

    return final_word_list