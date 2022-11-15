import jieba
import logging
import copy
from . import syllables
from . import logic

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
        syllable = syllables.PassThroughSyllable(current_character)
        new_solution = copy.copy(current_solution)
        new_solution.append(syllable)
        fill_pinyin_solution_for_characters(data, remaining_characters, new_solution, all_solutions)        

def get_pinyin_solutions_for_characters(data, word):
    all_solutions = []
    fill_pinyin_solution_for_characters(data, word, [], all_solutions)
    return all_solutions

def get_pinyin_solutions_for_word(data, word):
    entry = data.pinyin_map.get(word, None)
    if entry != None:
        logger.debug(f'located {word} as word')
        return [mapping.syllables for mapping in entry]
    else:
        logger.debug(f'breaking down {word} into characters')
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

    # apply tone change logic
    expanded_solution_list = [logic.apply_pinyin_tone_change(word_list, solution) for solution in expanded_solution_list]

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

def convert_pinyin(data, text, tone_numbers, spaces):
    solution_list = []
    word_list = tokenize(text)
    return render_all_pinyin_solutions(data, word_list, tone_numbers, spaces)


def tokenize(text):
    seg_list = jieba.cut(text)
    word_list = list(seg_list)
    return word_list
