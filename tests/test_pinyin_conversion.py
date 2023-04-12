import unittest
import pytest
import sys
import os
import json
import pprint
import requests
import logging

logger = logging.getLogger(__file__)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pinyin_jyutping
import pinyin_jyutping.parser
import pinyin_jyutping.errors

"""this file contains final end-to-end conversion tests on real data"""
class PinyinConversion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        cls.pinyin_jyutping = pinyin_jyutping.PinyinJyutping()

    def test_character_conversion(self):
        self.assertEqual(self.pinyin_jyutping.pinyin_all_solutions('了'), [['le', 'liǎo', 'liào']])

    def test_simple_pinyin(self):
        self.assertEqual(self.pinyin_jyutping.pinyin('没有'), 'méiyǒu')
        # self.assertEqual(self.pinyin_jyutping.pinyin('忘拿'), ['wàng ná'])

    def test_many_solutions(self):
        # pytest tests/test_pinyin_conversion.py -k test_many_solutions -s -rPP  --log-cli-level=DEBUG
        input_str = '对不起，这个字我会读，不会写。'
        expected_output = [
            ['duìbuqǐ'],
            ['，'],
            ['zhège'],
            ['zì', 'zi'],
            ['wǒhuì', 'wǒkuài'],
            ['dú', 'dòu'],
            ['，'],
            ['búhuì'],
            ['xiě', 'xiè'],
            ['。']
        ]
        output = self.pinyin_jyutping.pinyin_all_solutions(input_str)
        logger.debug(f'output: {pprint.pformat(output)}')
        self.assertEqual(output, expected_output)

    def test_simple_pinyin_traditional(self):
        self.assertEqual(self.pinyin_jyutping.pinyin('上課'), 'shàngkè')

    def test_pinyin_non_recognized_chars(self):
        # pytest --log-cli-level=DEBUG tests/test_pinyin_conversion.py -k test_pinyin_non_recognized_chars
        self.assertEqual(self.pinyin_jyutping.pinyin('請問，你叫什麼名字？'), 'qǐngwèn ， nǐ jiào shénme míngzi ？')
        self.assertEqual(self.pinyin_jyutping.pinyin_all_solutions('請問，你叫什麼名字？'), 
            [
                ['qǐngwèn'],
                ['，'],
                ['nǐ'],
                ['jiào'],
                ['shénme'],
                ['míngzi', 'míngzì'],
                ['？']
            ]
            )


    def test_simple_chars(self):
        self.assertEqual(self.pinyin_jyutping.pinyin('忘'), 'wàng')

    # @pytest.mark.skip(reason="too many alternatives")
    def test_pinyin_sentences(self):
        self.assertEqual(self.pinyin_jyutping.pinyin('忘拿一些东西了'), 'wàng ná yīxiē dōngxī le')
        self.assertEqual(self.pinyin_jyutping.pinyin('忘拿一些东西了', tone_numbers=True), 'wang4 na2 yi1xie1 dong1xi1 le5')
        self.assertEqual(self.pinyin_jyutping.pinyin('忘拿一些东西了', tone_numbers=True, spaces=True), 'wang4 na2 yi1 xie1 dong1 xi1 le5')
        self.assertEqual(self.pinyin_jyutping.pinyin('投资银行', tone_numbers=False, spaces=True), 'tóu zī yín háng')
        
        self.assertIn('bùjǐn 。 。 。 ,   hái ...', self.pinyin_jyutping.pinyin('不仅。。。, 还...', tone_numbers=False, spaces=False))

    def test_tone_changes(self):
        # pytest tests/test_pinyin_conversion.py -k test_tone_changes -s -rPP  --log-cli-level=DEBUG
        self.assertEqual(self.pinyin_jyutping.pinyin('穿不上'), 'chuān bú shàng')
        self.assertEqual(self.pinyin_jyutping.pinyin('不够亮'), 'búgòu liàng')
        self.assertEqual(self.pinyin_jyutping.pinyin('不成熟'), 'bù chéngshú')
        # dosen't seem to be applied by azure
        # self.assertEqual(self.pinyin_jyutping.pinyin('一起')[0], 'yìqǐ')
        self.assertEqual(self.pinyin_jyutping.pinyin('一个'), 'yígè')

    def test_pinyin_conversion_data_1(self):
        # large test 
        json_file_path = os.path.join(os.path.dirname(__file__), '..', 'source_data', 'pinyin_conversion_test_data_1.json')
        f = open(json_file_path, 'r')
        test_data = json.load(f)
        f.close()
        for entry in test_data:
            chinese = entry['chinese']
            expected_pinyin = entry['expected_pinyin']

            expected_pinyin = pinyin_jyutping.parser.clean_romanization(expected_pinyin)
            converted_pinyin = pinyin_jyutping.parser.clean_romanization(self.pinyin_jyutping.pinyin(chinese, spaces=True))

            expected_pinyin_syllables = pinyin_jyutping.parser.parse_pinyin(expected_pinyin)
            converted_pinyin_syllables = pinyin_jyutping.parser.parse_pinyin(converted_pinyin)

            self.assertEqual(expected_pinyin_syllables, converted_pinyin_syllables, f'chinese: {chinese}')


    def test_alternatives(self):
        # self.assertEqual(self.pinyin_jyutping.pinyin('举起来'), ['jǔ qǐ lai'])
        # 往后面坐
        self.assertEqual(self.pinyin_jyutping.pinyin_all_solutions('往后面坐'), 
                         [
                            ['wǎnghòu'],
                            ['miàn', 'mian'], 
                            ['zuò']
                        ])


    def test_user_corrections(self):
        # apply corrections
        pinyin_jyutping_instance_1 = pinyin_jyutping.PinyinJyutping()
        pinyin_jyutping_instance_1.load_pinyin_corrections(
            [
                {
                    'chinese': '东西',
                    'pinyin': 'dong1xi5' # make tone 5 / neutral the default
                }
            ]
        )
        self.assertEqual(pinyin_jyutping_instance_1.pinyin('忘拿一些东西了'), 'wàng ná yīxiē dōngxi le')


    def get_baserow_records(self):
        more_results = True

        records = []

        url = "https://api.baserow.io/api/database/rows/table/114466/?user_field_names=true&size=200"
        while more_results == True:
            logger.info(f'get_baserow_records querying url {url}')
            # load baserow table
            response = requests.get(
                url,
                headers={
                    "Authorization": f"Token {os.environ['BASEROW_API_TOKEN']}"
            })
            if response.status_code != 200:
                raise Exception(response.content)
            data = response.json()

            results = data['results']
            logger.info(f'received {len(results)} records')
            records.extend(results)

            more_results = data['next'] != None
            url = data['next']

        return records

    def get_baserow_records_map(self):
        records = self.get_baserow_records()
        result = {}
        for record in records:
            result[record['chinese']] = record
        return result


    def update_baserow_records(self, records):
        response = requests.patch(
            "https://api.baserow.io/api/database/rows/table/114466/batch/?user_field_names=true",
            headers={
                "Authorization": f"Token {os.environ['BASEROW_API_TOKEN']}",
                "Content-Type": "application/json"
            },
            json={
                "items": records
            }        
        )
        if response.status_code != 200:
            raise Exception(response.content)


    @pytest.mark.skipif('COMPARE_ANKI_DECKS' not in os.environ, reason="set COMPARE_ANKI_DECKS=yes")
    def test_compare_anki_decks(self):
        # COMPARE_ANKI_DECKS=yes BASEROW_API_TOKEN=<api token> pytest tests/test_pinyin_conversion.py -k test_compare_anki_decks -s -rPP  --log-cli-level=INFO
        # optionally set DEBUG_WORD="最主要的理由是..."
        filename = 'source_data/anki_deck_1.json'
        f = open(filename)
        data = json.load(f)
        f.close()

        baserow_record_map = self.get_baserow_records_map()
        record_updates = []

        def syllable_match_except_tones(syllable_a, syllable_b):
            return syllable_a.initial == syllable_b.initial and \
               syllable_a.final == syllable_b.final

        def syllable_list_match_except_tones(syllables_a, syllables_b):
            matches = [syllable_match_except_tones(syl_a, syl_b) for syl_a, syl_b in zip(syllables_a, syllables_b)]
            return all(matches)


        debug_word = False
        if 'DEBUG_WORD' in os.environ:
            debug_word = os.environ['DEBUG_WORD']

        for record in data:
            chinese = record['chinese']

            if debug_word != False:
                if chinese != debug_word:
                    continue

            logger.debug(f'processing chinese: {chinese}')

            expected_pinyin = pinyin_jyutping.parser.clean_romanization(record['pinyin'])
            all_results = self.pinyin_jyutping.pinyin(chinese, spaces=True)
            all_cleaned_pinyin_results = [pinyin_jyutping.parser.clean_romanization(result) for result in all_results]
            converted_pinyin = all_cleaned_pinyin_results[0]

            logger.debug(f'result: {converted_pinyin}')

            try:
                expected_pinyin_syllables = pinyin_jyutping.parser.parse_pinyin(expected_pinyin)
                converted_pinyin_syllables = pinyin_jyutping.parser.parse_pinyin(converted_pinyin)
                converted_pinyin_syllable_all_results = [pinyin_jyutping.parser.parse_pinyin(result) for result in all_cleaned_pinyin_results]

                status = 313817 # failure
                if expected_pinyin_syllables == converted_pinyin_syllables:
                    status = 313816 # success
                elif expected_pinyin_syllables in converted_pinyin_syllable_all_results:
                    # is the result present in one of these alternatives ?                    
                    status = 317360 # alternative
                elif syllable_list_match_except_tones(expected_pinyin_syllables, converted_pinyin_syllables):
                    # tone mismatch only
                    status = 317826

                record_updates.append({
                    'id': baserow_record_map[chinese]['id'],
                    'expected_pinyin': expected_pinyin,
                    'expected_syllables': str(expected_pinyin_syllables),
                    'converted_pinyin': converted_pinyin,
                    'converted_pinyin_syllables': str(converted_pinyin_syllables),
                    'status': status
                })            

            except pinyin_jyutping.errors.PinyinParsingError as e:
                # despite the parsing error, is the converted pinyin same as the expected ?
                if expected_pinyin == converted_pinyin:
                    record_updates.append({
                        'id': baserow_record_map[chinese]['id'],
                        'status': 313816, # success
                        'converted_pinyin': converted_pinyin,
                    })
                else:
                    logger.exception(e)
                    record_updates.append({
                        'id': baserow_record_map[chinese]['id'],
                        'status': 317659 # exception
                    })                            

            if len(record_updates) >= 100:
                logger.info('flushing baserow updates')
                # flush to baserow
                self.update_baserow_records(record_updates)
                record_updates = []
                
        logger.info('flushing remaining baserow updates')
        # flush to baserow
        self.update_baserow_records(record_updates)
        record_updates = []        

    def test_convert_pinyin_single_solution(self):
        # pytest --log-cli-level=DEBUG tests/test_pinyin_conversion.py -k test_convert_pinyin_single_solution
        self.assertEqual(self.pinyin_jyutping.pinyin('没有'), 'méiyǒu')
        self.assertEqual(self.pinyin_jyutping.pinyin('没有', spaces=True), 'méi yǒu')
        self.assertEqual(self.pinyin_jyutping.pinyin('没有', tone_numbers=True), 'mei2you3')
        self.assertEqual(self.pinyin_jyutping.pinyin('没有', tone_numbers=True, spaces=True), 'mei2 you3')
        self.assertEqual(self.pinyin_jyutping.pinyin('請問，你叫什麼名字？'), 'qǐngwèn ， nǐ jiào shénme míngzi ？')

    def test_multiline_input(self):
        # pytest --log-cli-level=DEBUG tests/test_pinyin_conversion.py -k test_multiline_input

        input = """没有
請問，你叫什麼名字？"""
        expected_output = """méiyǒu 
 qǐngwèn ， nǐ jiào shénme míngzi ？"""
        output = self.pinyin_jyutping.pinyin(input)
        self.assertEqual(output, expected_output)


    # @pytest.mark.skip(reason="skip for now")
    def test_long_input(self):
        # pytest --log-cli-level=DEBUG tests/test_pinyin_conversion.py -k test_long_input

        input = """
1.在野外要进入草丛时，切记要先打草惊蛇。
2、你最好别打草惊蛇，老板很喜欢peter，而你只是没没无闻的小人物。还是放聪明点儿，别吭声，等待时机。
3、警方守候多日，就是怕打草惊蛇，让歹徒溜了。
4、连长告诉我们,不要打草惊蛇,要对敌人进行围攻。
5、你打草惊蛇了惊什么蛇？
6、我爬山时一定带根棍子，既可以当柺杖，又可以打草惊蛇。
7、这个计谋的关键在于避免打草惊蛇，等对方松懈后，可一举进攻。
7、造 句 网zaojv.com是一部在线造句词典,其宗旨是让大家更快地造出更优秀的句子.
8、对方似仍未察觉，我们先按兵不动，免得打草惊蛇。
9、最后他们决定最好不要打草惊蛇并且不再进一步讨论这个问题。
10、他的第二个冲动是不必打草惊蛇。
11、你这样轻举妄动只会打草惊蛇，给下一步的工作带来困难。
12、大家先不动声色，免得打草惊蛇，让他跑了。
13、我爬山时一定带根棍子，既可以当拐杖，又可以打草惊蛇。
14、你调动这么多警力，岂不打草惊蛇？歹徒当然早就跑掉了。
15、这个计谋的关键在于避免打草惊蛇，等对方鬆懈后，可一举进攻。
16、记者象是一群狗，但有打草惊蛇，就开端吠个不绝。
17、我是说我不想打草惊蛇zaojv.com。
18、为了不打草惊蛇，他只是旁敲侧击地询问了来人几个问题。
19、侦破工作应谨慎保密，不要打草惊蛇。
20、这是敌人的先头部队，放他们过去，以免打草惊蛇，影响全歼敌人主力的计划。
21、这次行动千万要保密,不能打草惊蛇。
22、消息指她们都比平日"格外小心"，以免打草惊蛇，故媒体也未能得知她们的身份。
23、这件事得不动声色慢慢跟他磨，否则一打草惊蛇后，很难说服他。
24、警方为了避免打草惊蛇，所以派出便衣警察埋伏在四周。
25、这件事急不得，表面要装镇定，以免打草惊蛇。
26、不要做那种打草惊蛇的蠢事，不动则已，要动就必须使罪犯全部落网。
27、小偷已经进来了，所以最好不要打草惊蛇，免着他发现家里有人。
28、你就打听些这样的小消息，还让我埋伏的死士都给暴光了，打草惊蛇了还想要报酬啊。
29、现在的局势非常紧张，我们要不动声色的观察敌情，以免打草惊蛇。
30、他们不得不自污其行，对那些奸臣们虚与委蛇，为的是获得为国尽忠的机会，免得打草惊蛇，四面树敌，以致遭受奸臣们的嫉恨与陷害。        
        """
        output = self.pinyin_jyutping.pinyin(input)

        # count number of lines
        lines = output.split('\n')
        self.assertEqual(len(lines), 33)  # including lines above,below
