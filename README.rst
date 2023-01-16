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

>>> import pinyin_jyutping
>>> p = pinyin_jyutping.PinyinJyutping()
>>> p.pinyin('忘拿一些东西了')[0]
'wàng ná yīxiē dōngxī le'
>>> p.pinyin('忘拿一些东西了', tone_numbers=True)[0]
'wang4 na2 yi1xie1 dong1xi1 le5'    
>>> p.pinyin('忘拿一些东西了', tone_numbers=True, spaces=True)[0]
'wang4 na2 yi1 xie1 dong1 xi1 le5'    

**Jyutping**

>>> import pinyin_jyutping
>>> j = pinyin_jyutping.PinyinJyutping()
>>> j.jyutping('我出去攞野食')[0]
'ngǒ cēothêoi ló jěsik'
>>> j.jyutping('我出去攞野食', tone_numbers=True)[0]
'ngo5 ceot1heoi3 lo2 je5sik6'
>>> j.jyutping('我出去攞野食', tone_numbers=True, spaces=True)[0]
'ngo5 ceot1 heoi3 lo2 je5 sik6'    

How it works
------------

Uses the Jieba library (https://github.com/fxsjy/jieba) to tokenize the sentence. Then words are converted to Pinyin/Jyutping either as a whole, or character by character, using the CC-Canto dictionary (http://cantonese.org/about.html). The Jyutping diacritic conversion is not standard but originally described here: http://www.cantonese.sheik.co.uk/phorum/read.php?1,127274,129006

