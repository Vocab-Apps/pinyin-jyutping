import jieba


def convert_pinyin(data, text, tone_numbers, spaces):
    result_words = []
    word_list = tokenize(text)
    for word in word_list:
        if word in data.word_map:
            pinyin = ''.join([x.render_tone_number() for x in data.word_map[word][0].syllables])
            result_words.append(pinyin)
    return ' '.join(result_words)

def tokenize(text):
    seg_list = jieba.cut(text)
    word_list = list(seg_list)
    return word_list
