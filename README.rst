pinyin-jyutping
===============

Python module which converts a Chinese sentence from Simplified/Traditional to Mandarin/Pinyin and Traditional/Simplified to Cantonese/Jyutping, outputting diacritics (accented characters). I designed this library to create Mandarin and Cantonese flashcards.

Want to support my work on this module ? Become a supporter: https://www.patreon.com/lucw

Install
-------

.. code:: bash

    $ pip install pinyin_jyutping

Usage
-----

**Pinyin**

generate the best solution:

>>> import pinyin_jyutping
>>> p = pinyin_jyutping.PinyinJyutping()
>>> p.pinyin('忘拿一些东西了')
'wàng ná yīxiē dōngxī le'
>>> p.pinyin('忘拿一些东西了', tone_numbers=True)
'wang4 na2 yi1xie1 dong1xi1 le5'    
>>> p.pinyin('忘拿一些东西了', tone_numbers=True, spaces=True)
'wang4 na2 yi1 xie1 dong1 xi1 le5'    

generate all possible solutions:

>>> import pinyin_jyutping
>>> p = pinyin_jyutping.PinyinJyutping()
>>> p.pinyin_all_solutions('忘拿一些东西了')
{'word_list': ['忘', '拿', '一些', '东西', '了'], 'solutions': [['wàng'], ['ná'], ['yīxiē'], ['dōngxī', 'dōngxi'], ['le', 'liǎo', 'liào']]}

**Jyutping**

generate the best solution:

>>> import pinyin_jyutping
>>> j = pinyin_jyutping.PinyinJyutping()
>>> j.jyutping('我出去攞野食')
'ngǒ cēothêoi ló jěsik'
>>> j.jyutping('我出去攞野食', tone_numbers=True)
'ngo5 ceot1heoi3 lo2 je5sik6'
>>> j.jyutping('我出去攞野食', tone_numbers=True, spaces=True)
'ngo5 ceot1 heoi3 lo2 je5 sik6'    

generate all possible solutions:

>>> import pinyin_jyutping
>>> j = pinyin_jyutping.PinyinJyutping()
>>> j.jyutping_all_solutions('我出去攞野食')
{'word_list': ['我', '出去', '攞', '野食'], 'solutions': [['ngǒ'], ['cēothêoi'], ['ló', 'lō'], ['jěsik', 'jězi', 'jěsit', 'jězik']]}

How it works
------------

Uses the Jieba library (https://github.com/fxsjy/jieba) to tokenize the sentence. Then words are converted to Pinyin/Jyutping either as a whole, or character by character, using the CC-Canto dictionary (http://cantonese.org/about.html). The Jyutping diacritic conversion is not standard but originally described here: http://www.cantonese.sheik.co.uk/phorum/read.php?1,127274,129006

