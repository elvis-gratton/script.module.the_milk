# tests.py
from the_milk.modules import source_utils

class Tests:

    def __init__(self):
        self.debug = False
        self._debug_it('Init')

    def _debug_it(self, msg, caller=None):
        if self.debug:
            from the_milk.modules.log_utils import log
            log('TESTS | %s' % msg, caller)

    def data_movie_1(self):
        data = {
            'aliases': [
                {'title': 'Puss in Boots 2: Nine Lives & 40 Thieves', 'country_code': 'US'},
                {'title': '장화 신은 고양이 2', 'country_code': 'KR'},
                {'title': 'Mačak u čizmama: Poslednja želja', 'country_code': 'RS'},
                {'title': 'החתול במגפיים 2: משאלה אחת ודי', 'country_code': 'IL'},
                {'title': 'بوس إن بوتز: ذا لاست ويش', 'country_code': 'SA'},
                {'title': 'قط في أحذية : الأمنية الأخيرة', 'country_code': 'SA'},
                {'title': 'החתול במגפיים: משאלה אחת ודי', 'country_code': 'IL'},
                {'title': 'החתול של שרק: משאלה אחת ודי', 'country_code': 'IL'},
                {'title': 'Puss in Boots: The Last Wish', 'country_code': 'CA'},
                {'title': 'Le Chat potté 2 : La Dernière Quête', 'country_code': 'FR'},
                {'title': 'Puss in Boots: The Last Wish', 'country_code': ''},
                {'title': 'Puss in Boots: The Last Wish', 'country_code': 'US'}],
            'year': '2022',
            'title': 'Le Chat potté 2 : La Dernière Quête'
        }
        return data

    def data_serie_1(self):
        data = {
            'aliases': [{'title': 'La liste noire', 'country_code': 'CA'},
                        {'title': 'Blacklist', 'country_code': 'UK'},
                        {'title': 'THE BLACKLIST/ブラックリスト', 'country_code': 'JP'},
                        {'title': 'THE BLACKLIST ブラックリスト', 'country_code': 'JP'},
                        {'title': 'Черный список', 'country_code': 'RU'},
                        {'title': 'Kara Liste', 'country_code': 'TR'}],
            'season': '9',
            'episode': '1',
            'year': '',
            'title': 'S09E01',
            'tvshowtitle': 'the blacklist'
        }
        return data

    def data_serie_2(self):
        data = {
            "aliases":
                [{'title': 'আমাদের শেষ', 'country_code': 'BD'},
                 {'title': 'the last of us: последните оцелели', 'country_code': 'BG'},
                 {'title': "les derniers d'entre nous", 'country_code': 'CH'},
                 {'title': '最后幸存者', 'country_code': 'CN'},
                 {'title': 'poslední z nás', 'country_code': 'CZ'}, {'title': 'de sidste som os', 'country_code': 'DK'},
                 {'title': 'los últimos de nosotros', 'country_code': 'ES'},
                 {'title': 'האחרונים מבנינו', 'country_code': 'IL'},
                 {'title': 'האחרונים שביננו', 'country_code': 'IL'},
                 {'title': 'האחרונים שמבינינו', 'country_code': 'IL'},
                 {'title': 'آخرین بازمانده\u200cی ما', 'country_code': 'IR'},
                 {'title': 'آخرین ما', 'country_code': 'IR'},
                 {'title': 'ザ・ラスト・オブ・アス', 'country_code': 'JP'}, {'title': 'ラスト・オブ・アス', 'country_code': 'JP'},
                 {'title': 'ラスアス', 'country_code': 'JP'}, {'title': '더 라스트 오브 어스', 'country_code': 'KR'},
                 {'title': 'paskutiniai iš mūsų', 'country_code': 'LT'}, {'title': 'одни из нас', 'country_code': 'RU'},
                 {'title': 'posledný z nás', 'country_code': 'SK'}, {'title': 'ปัจฉิมอเมริกา', 'country_code': 'TH'},
                 {'title': 'bizden geriye kalanlar', 'country_code': 'TR'},
                 {'title': '最後生還者', 'country_code': 'TW'},
                 {'title': 'останні з нас', 'country_code': 'UA'},
                 {'title': 'những người còn sót lại', 'country_code': 'VN'},
                 {'title': 'the last of us', 'country_code': ''}, {'title': 'the last of us', 'country_code': 'US'}],
            'season': '1',
            'episode': '1',
            'year': '',
            'title': 'S01E01',
            'tvshowtitle': 'the last of us'
        }
        return data

    def data_serie_packs_1(self):
        data = {
            "aliases":
                [{'title': 'আমাদের শেষ', 'country_code': 'BD'},
                 {'title': 'the last of us: последните оцелели', 'country_code': 'BG'},
                 {'title': "les derniers d'entre nous", 'country_code': 'CH'},
                 {'title': '最后幸存者', 'country_code': 'CN'},
                 {'title': 'poslední z nás', 'country_code': 'CZ'}, {'title': 'de sidste som os', 'country_code': 'DK'},
                 {'title': 'los últimos de nosotros', 'country_code': 'ES'},
                 {'title': 'האחרונים מבנינו', 'country_code': 'IL'},
                 {'title': 'האחרונים שביננו', 'country_code': 'IL'},
                 {'title': 'האחרונים שמבינינו', 'country_code': 'IL'},
                 {'title': 'آخرین بازمانده\u200cی ما', 'country_code': 'IR'},
                 {'title': 'آخرین ما', 'country_code': 'IR'},
                 {'title': 'ザ・ラスト・オブ・アス', 'country_code': 'JP'}, {'title': 'ラスト・オブ・アス', 'country_code': 'JP'},
                 {'title': 'ラスアス', 'country_code': 'JP'}, {'title': '더 라스트 오브 어스', 'country_code': 'KR'},
                 {'title': 'paskutiniai iš mūsų', 'country_code': 'LT'}, {'title': 'одни из нас', 'country_code': 'RU'},
                 {'title': 'posledný z nás', 'country_code': 'SK'}, {'title': 'ปัจฉิมอเมริกา', 'country_code': 'TH'},
                 {'title': 'bizden geriye kalanlar', 'country_code': 'TR'},
                 {'title': '最後生還者', 'country_code': 'TW'},
                 {'title': 'останні з нас', 'country_code': 'UA'},
                 {'title': 'những người còn sót lại', 'country_code': 'VN'},
                 {'title': 'the last of us', 'country_code': ''}, {'title': 'the last of us', 'country_code': 'US'}],
            'season': '1',
            'episode': '',
            'imdb': 'tt3581920',
            'year': '',
            'title': 'saison 1',
            'tvshowtitle': 'the last of us'
        }
        return data

    def data_serie_packs_2(self):
        data = {
            'aliases': [{'title': 'La liste noire', 'country_code': 'CA'},
                        {'title': 'Blacklist', 'country_code': 'UK'},
                        {'title': 'THE BLACKLIST/ブラックリスト', 'country_code': 'JP'},
                        {'title': 'THE BLACKLIST ブラックリスト', 'country_code': 'JP'},
                        {'title': 'Черный список', 'country_code': 'RU'},
                        {'title': 'Kara Liste', 'country_code': 'TR'}],
            'season': '1',
            'episode': '',
            'imdb': 'tt2741602',
            'year': '',
            'title': 'saison 1',
            'tvshowtitle': 'the Blacklist'
        }
        return data

    def _test_hash_1(self):
        data1_in32 = 'UVC5SFG7E4LBTDWVATDXVXD6HZVLBPGE'
        data1_out40 = '4AA8F1D4279DF7DF3BE3B68280E19ACFD6A7A165'
        magnet1_url = 'magnet:?xt=urn:btih:JKUPDVBHTX356O7DW2BIBYM2Z7LKPILF'

        data2_in40 = 'E76D6456443A326521824C2765A07F6989396F5B'
        data2_out40 = 'E76D6456443A326521824C2765A07F6989396F5B'
        magnet1_url = 'magnet:?xt=urn:btih:E76D6456443A326521824C2765A07F6989396F5B'

        # result = source_utils.hash_is_valid(data1_in32)
        # result_hash = source_utils.base32_to_hex(data1_in32, 'TORRENT9 test_hash 16bytes')
        result_hash = source_utils.base32_to_hex(data1_in32, '-')

        # result = source_utils.hash_is_valid(data2_in40)
        # result_hash = source_utils.base32_to_hex(data2_in40, '-')
        result_hash = source_utils.base32_to_hex(data2_in40, '-')
        return

    def _main(self):
        pass


if __name__ == "__main__":
    zit = Tests()
    zit._main()
