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
            'genre': 'Animation',
            'original_title': 'PUSS IN BOOTS THE LAST WISH',
            'title': 'Le Chat potté 2 : La Dernière Quête'
        }
        return data

    def data_movie_2(self):
        data = {
            'aliases': [
                {"country_code": "LV", "title": "Doktors Streindžs neprāta multivisumā"},
                {"country_code": "US", "title": "Doctor Strange in the Multitude of Madness 3D"},
                {"country_code": "KR", "title": "닥터 스트레인지 2"},
                {"country_code": "HK", "title": "奇異博士2: 失控多元宇宙"},
                {"country_code": "GR", "title": "Ο Δόκτωρ Στρέιντζ στο πολυσύμπαν της τρέλας"},
                {"country_code": "AZ", "title": "Doktor Streync 2: Multikainatın Dəliliklərində"},
                {"country_code": "US", "title": "Doctor Strange 2 - The Multiverse of Madness"},
                {"country_code": "CN", "title": "奇异博士2：疯狂多元宇宙"},
                {"country_code": "TW", "title": "奇異博士2：失控多重宇宙"},
                {"country_code": "BR", "title": "Doutor Estranho no Multiverso da Loucura"},
                {"country_code": "VN", "title": "Doctor Strange: Đa Vũ Trụ Hỗn Loạn"},
                {"country_code": "AM", "title": "Բժիշկ Սթրենջը Խելագարության Բազմաշխարհում"},
                {"country_code": "US", "title": "Stellar Vortex"},
                {"country_code": "GE", "title": "დოქტორი სტრეინჯი სიგიჟის მრავალსამყაროში"},
                {"country_code": "GE", "title": "დოქტორი სტრეინჯი სიგიჟის მულტივერსში"},
                {"country_code": "KR", "title": "마블 닥터 스트레인지: 대혼돈의 멀티버스"},
                {"country_code": "KR", "title": "닥터 스트레인지 대혼돈의 멀티버스"},
                {"country_code": "RO", "title": "Doctor Strange în Multiversul Nebuniei"},
                {"country_code": "FR", "title": "Doctor Strange 2 - Doctor Strange in the Multiverse of Madness"},
                {"country_code": "PL", "title": "Doktor Strange w multiwersum obłędu"},
                {"country_code": "IL", "title": "דר מוזר 2 במימדי השיגעון"},
                {"country_code": "FR", "title": "Marvel Film 28 - Doctor Strange in the Multiverse of Madness"}
                ],
                'year': '2022',
                'genre': 'fiction',
                'original_title': 'Doctor Strange in the Multiverse of Madness',
                'title': 'Doctor Strange in the Multiverse of Madness'
        }
        return data

    def data_movie_3(self):
        data = {
            'aliases': [
                {"country_code": "LV", "title": "Doktors Streindžs"},
                {"country_code": "US", "title": "Doctor Strange"},
                {"country_code": "KR", "title": "닥터 스트레인지"},
                {"country_code": "HK", "title": "奇異博士: 失控多元宇宙"},
                {"country_code": "AZ", "title": "Doktor Streync"},
                {"country_code": "US", "title": "Doctor Strange"},
                {"country_code": "CN", "title": "奇异博士"},
                {"country_code": "TW", "title": "奇異博士"},
                {"country_code": "BR", "title": "Doutor Estranho"},
                {"country_code": "VN", "title": "Doctor Strange"},
                {"country_code": "RO", "title": "Doctor Strange"},
                {"country_code": "FR", "title": "Doctor Strange"},
                {"country_code": "PL", "title": "Doktor Strange"},
                {"country_code": "IL", "title": "במימדי השיגעון"},
                {"country_code": "FR", "title": "Marvel Film Doctor Strange"}
                ],
                'year': '2016',
                'genre': 'Fiction',
                'original_title': 'Doctor Strange',
                'title': 'Doctor Strange'
        }
        return data

    def data_movie_4(self):
        data = {
            "aliases": [
                {"title": "аватар 2", "country_code": "RU"}, 
                {"title": "isikunijimas 2", "country_code": "LT"},
                {"title": "avatar 2", "country_code": "US"}, 
                {"title": "아바타 2", "country_code": "KR"},
                {"title": "аватар 2", "country_code": "UA"}, 
                {"title": "アハター ウェイ・オフ・ウォーター", "country_code": "JP"},
                {"title": "افاتار: طريق المياه", "country_code": "AE"}, 
                {"title": "ଅବତାର ୨", "country_code": "IN"},
                {"title": "аватар: путь воды", "country_code": "RU"},
                {"title": "avatar: el sentit de l'aigua", "country_code": "AD"},
                {"title": "avatar: the way of water 2022", "country_code": ""},
                {"title": "avatar : la voie de l'eau 2022", "country_code": "US"}
                ],
                "year": "2022",
                'genre': 'Fiction',
                'original_title': "avatar  la voie de l'eau",
                'title': "avatar  la voie de l'eau"
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
            'genre': 'Drame',
            'original_title': 'the blacklist',
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
            'genre': 'Drame',
            'original_title': 'the last of us',
            'tvshowtitle': 'the last of us'
        }
        return data

    def data_serie_3(self):
        data = {
            "aliases"    :
                [],
            'season'     : '5',
            'episode'    : '1',
            'year'       : '',
            'title'      : 'S05E01',
            'genre'      : 'Drame',
            'original_title': 'yellowstone',
            'tvshowtitle': 'yellowstone'
        }
        return data

    def data_serie_4(self):
        data = {
            "aliases"       :
                [{'title': 'citadelle', 'country_code': 'FR'}, {'title': 'ซทาเดล', 'country_code': 'TH'}, {'title': 'citadel 2023', 'country_code': ''}, {'title': 'citadelle 2023', 'country_code': 'US'}],
            'season'        : '1',
            'episode'       : '1',
            'year'          : '',
            'title'         : 'S01E01',
            'genre'         : 'Drame',
            'original_title': 'citadel',
            'tvshowtitle'   : 'citadelle'
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
            'genre': 'Drame',
            'original_title': 'the last of us',
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
            'genre': 'Drame',
            'original_title': 'the Blacklist',
            'tvshowtitle': 'the Blacklist'
        }
        return data

    def data_serie_packs_3(self):   # la petite vie
        data = {
            'aliases': [],
            'season': '1',
            'episode': '',
            'imdb': 'tt2741602',
            'year': '',
            'title': 'saison 1',
            'genre': 'Comedie',
            'original_title': 'la petite vie',
            'tvshowtitle': 'la petite vie'
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
