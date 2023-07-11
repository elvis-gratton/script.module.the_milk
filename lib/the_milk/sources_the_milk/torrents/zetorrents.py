# -*- coding: utf-8 -*-
# Fork of Projects from Venom Fenomscrapers, TikiPeter FEN, CocoJoe2411 cocoscrapers

import re
from urllib.parse import quote_plus
from the_milk.modules import client
from the_milk.modules import source_utils
from the_milk.modules import workers
from the_milk.modules import log_utils
from the_milk.modules.cleantitle import normalize
# from libs.web_pdb import WebPdb


class source:
    priority = 5
    pack_capable = True
    has_movies = True
    has_episodes = True

    def __init__(self):
        self.language = ['fr']
        self.base_link = "https://www.zetorrents.pw"
        self.search_link = '/recherche'
        self.films_link = '/films'
        self.series_link = '/series'
        self.min_seeders = 0
        self.debug = False
        self._debug_it('Init')

    def _debug_it(self, msg, caller=None):
        if self.debug:
            log_utils.log('zeTORRENTS | %s' % msg, caller, 1)


    def sources(self, data, host_dict):
        self.sources = []
        if not data:
            self._debug_it('sources: no data')
            return self.sources

        self.sources_append = self.sources.append
        try:
            self.aliases = data['aliases']
            if 'tvshowtitle' in data:
                l_title = data['tvshowtitle'].lower().replace('&', 'and').replace('/', '-').replace('$', 's')
                self.title = normalize(l_title)
                self.episode_title = data['title'].lower()
                self.is_movie = False
                self.year = ''
                self.hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode']))
                self.years = None
            else:
                l_title = data['title'].lower().replace('&', 'and').replace('/', '-').replace('$', 's')
                self.title = normalize(l_title)
                self.episode_title = None
                self.is_movie = True
                self.year = data['year']
                self.hdlr = self.year
                try:
                    self.years = [str(int(self.year)), str(int(self.year)-1), str(int(self.year) + 1)]
                except:
                    self.years = None

            self._debug_it('sources: LT=%s T=%s Y=%s H=%s A=%s' % (l_title, self.title, self.year, self.hdlr, self.aliases))

            self.undesirables = source_utils.get_undesirables()
            self.check_foreign_audio = source_utils.check_foreign_audio()

            if self.is_movie:
                queries = [
                    '%s%s/%s' % (self.base_link, self.search_link, quote_plus('%s %s' % (l_title, self.years[0]))),
                    '%s%s/%s' % (self.base_link, self.search_link, quote_plus('%s %s' % (l_title, self.years[1]))),
                    '%s%s/%s' % (self.base_link, self.search_link, quote_plus('%s %s' % (l_title, self.years[2])))
                ]
            else:
                queries = [
                    '%s%s/%s' % (self.base_link, self.search_link, quote_plus(l_title))
                ]
            threads = []
            append = threads.append
            for link in queries:
                append(workers.Thread(self.get_sources, link))

            [i.start() for i in threads]
            [i.join() for i in threads]
            return self.sources
        except Exception as e:
            source_utils.scraper_error('ZETORRENTS %s' % str(e))
            return self.sources

    def get_sources(self, link):
        link = re.sub(r'[\n\t]', '', link)

        try:
            results = client.request(link, timeout=5)
        except Exception as e:
            log_utils.error('get_sources: https request search item %s' % str(e))

        if not results or 'Pas de torrents disponibles correspondant à votre recherche' in results:
            return

        if '<tbody' not in results:
            return

        table = client.parseDOM(results, 'tbody')
        if not table or len(table) == 0:
            return
        table = table[0]

        rows = client.parseDOM(table, 'tr')
        if not rows:
            return
        self._debug_it('get_sources: tr parsing done rows=%s' % len(rows))
        self._debug_it('-')

        for row in rows:

            name = re.findall('title="(.*?)"', row)
            if not name:
                continue
            name = normalize(name[0]).replace(' en torrent', '').replace('(version longue)', '').replace(
                'version longue', '').replace('extended', '').replace('amzn', '')

            url = re.findall('href="(.*?)"', row)
            if not url:
                continue
            url = url[0]

            year_str = None
            t = re.split('french|truefrench|multi |vff|vfq', name, 1)
            if not t or len(t) < 2:
                continue

            year_str = re.findall("19\d\d|20\d\d", t[1])
            if year_str:
                file_title = str(t[0]) + str(year_str[0])
            else:
                file_title = str(t[0])

            self._debug_it('get_sources: T=%s FT=%s H=%s' % (self.title, file_title, self.hdlr))

            if not source_utils.check_title(self.title, self.aliases, file_title, self.hdlr, self.year, self.years):
                self._debug_it('get_sources: check_title FAILED!  T=%s FT=%s H=%s Y=%s YS=%s' % (
                self.title, file_title, self.hdlr, self.year, self.years))

                continue

            self._debug_it('get_sources: check_title OK!  T=%s FT=%s Y=%s A=%s' % (self.title, file_title, self.year, self.aliases))

            link = '%s%s' % (self.base_link, url)
            try:
                result_html = client.request(link, timeout=5)
            except:
                log_utils.error('https request page infos')
                continue

            if not result_html or 'magnet:?xt=urn:btih:' not in result_html:
                continue

            tbody = client.parseDOM(result_html, 'tbody')
            if not tbody or len(tbody) < 2:
                continue
            self._debug_it('get_sources: parsing done')

            name_info = source_utils.info_from_name(name, self.title, self.year, self.hdlr, self.episode_title)

            self._debug_it('get_sources: name_info=%s' % name_info)

            if source_utils.remove_lang(name_info, self.check_foreign_audio):
                continue
            if self.undesirables and source_utils.remove_undesirables(name_info, self.undesirables):
                continue

            seeders, dsize, isize, quality, info = 0, 0, 0, '', ''
            if not self.is_movie:
                ep_strings = [r'[.-]s\d{2}e\d{2}([.-]?)', r'[.-]s\d{2}([.-]?)', r'[.-]season[.-]?\d{1,2}[.-]?',
                              r'[.-]saison[.-]?\d{1,2}[.-]?']
                if any(re.search(item, name) for item in ep_strings):
                    continue

            detail = client.parseDOM(tbody[1], 'tr')
            if len(detail) < 2:
                continue
            try:
                seeders = int(re.findall('"retourSeeds">(.*?)</font>', detail[0])[0])
            except:
                seeders = 0

            quality, info = source_utils.get_release_quality(name_info, None)
            try:
                dsize, isize = source_utils._size(re.findall('<strong>(.*?)</strong>', detail[2])[0])
                info.insert(0, isize)
            except:
                dsize = 0
                info = ' | '.join(info)

            but_magnet = re.findall('href=\"(magnet.*?)\"', result_html)
            if not but_magnet:
                continue
            but_magnet = but_magnet[0]

            hash_magnet = re.findall('xt=urn:btih:(.*?)&tr', but_magnet)
            if not hash_magnet:
                continue
            hash_magnet = hash_magnet[0]

            self._debug_it('get_sources: magnet=%s' % but_magnet)
            self._debug_it('get_sources: Len=%s  hash=%s' % (len(hash_magnet), hash_magnet))

            if len(hash_magnet) == 32:
                try:
                    hash40 = source_utils.base32_to_hex(hash_magnet, 'get_sources')
                except:
                    continue
            else:
                hash40 = hash_magnet

            self._debug_it('get_sources: Len=%s  hash40=%s' % (len(hash40), hash40))
            but_magnet_link = 'magnet:?xt=urn:btih:%s' % hash40

            self.sources_append(
                {'provider': 'zetorrents', 'source': 'torrent', 'seeders': seeders, 'hash': hash40, 'name': name, 'name_info': name_info,
                 'quality': quality, 'language': 'fr', 'url': but_magnet_link, 'info': info, 'direct': False,'debridonly': True, 'size': dsize})

            self._debug_it('APPEND name=%s' % name)
            self._debug_it('APPEND magnet=%s' % but_magnet_link)
            self._debug_it(
                'APPEND seeders= %s hash= %s name= %s nameInfo= %s quality= %s size=%s url= %s' % (
                    seeders, hash40, name, name_info, quality, isize, but_magnet_link))
            self._debug_it('-')

    def sources_packs(self, data, host_dict, search_series=False, total_seasons=None, bypass_filter=False):
        self.sources = []
        if not data:
            return self.sources
        self._debug_it('sources_packs')
        self.sources_append = self.sources.append

        try:
            self.search_series = search_series
            self.total_seasons = total_seasons
            self.bypass_filter = bypass_filter

            l_title = data['tvshowtitle'].lower().replace('&', 'and').replace('/', ' ').replace('$', 's')
            self.title = normalize(l_title)
            self.aliases = data['aliases']
            self.imdb = data['imdb']
            self.year = data['year']
            self.season_x = data['season']
            self.season_xx = self.season_x.zfill(2)
            self.undesirables = source_utils.get_undesirables()
            self.check_foreign_audio = source_utils.check_foreign_audio()

            # query = re.sub(r'[^A-Za-z0-9\s\.-]+', '', self.title)
            if search_series:
                season_url = '%s%s/%s' % (self.base_link, self.search_link, quote_plus(l_title + ' saison'))
            else:
                season_url = '%s%s/%s' % (
                    self.base_link, self.search_link, quote_plus(l_title + ' saison %s' % self.season_x))

            threads = []
            append = threads.append
            append(workers.Thread(self.get_sources_packs, season_url))

            [i.start() for i in threads]
            [i.join() for i in threads]
            return self.sources


        except Exception as e:
            self._debug_it('sources_packs: Exception %s' % str(e))
            return self.sources

    def get_sources_packs(self, season_url):
        link = re.sub(r'[\n\t]', '', season_url)
        if not link:
            return

        try:
            results = client.request(link, timeout=5)
        except:
            log_utils.error('https request search Pack items')
            return
        if not results or '<tbody' not in results:
            return

        table = client.parseDOM(results, 'tbody')[0]
        if not table:
            return
        rows = client.parseDOM(table, 'tr')
        if not rows:
            return
        self._debug_it('get_sources_packs: tr parsing done rows=%s' % len(rows))
        self._debug_it('-')

        for row in rows:
            name = re.findall('title="(.*?)"', row)
            if not name:
                continue
            name = normalize(name[0]).replace(' en torrent', '').replace('amzn', '')

            url = re.findall('href="(.*?)"', row)
            if not url:
                continue
            url = url[0]

            year_name = None
            t = re.split('french|truefrench|multi |vff|vfq', name, 1)
            if not t or len(t) < 2:
                continue

            year_name = re.findall("19\d\d|20\d\d", t[1])
            if year_name:
                file_title = str(t[0]) + str(year_name[0])
            else:
                file_title = str(t[0])

            self._debug_it('get_sources_packs: T=%s N=%s' % (self.title, file_title))

            episode_start, episode_end, valid = 0, 0, False
            if not self.search_series:
                if not self.bypass_filter:
                    valid, episode_start, episode_end = source_utils.filter_season_pack(self.title, self.aliases,
                                                                                        self.year, self.season_x, name)
                    if not valid:
                        continue
                package = 'season'
            elif self.search_series:
                if not self.bypass_filter:
                    valid, last_season = source_utils.filter_show_pack(self.title, self.aliases, self.imdb, self.year,
                                                                       self.season_x, name, self.total_seasons)
                if not valid:
                    continue
            else:
                last_season = self.total_seasons
                package = 'show'

            self._debug_it('get_sources_packs: check_title OK!  T=%s N=%s' % (self.title, file_title))

            link = '%s%s' % (self.base_link, url)
            try:
                result_html = client.request(link, timeout=5)
            except:
                log_utils.error('https request page Pack infos')
                continue

            if not result_html or 'magnet:?xt=urn:btih:' not in result_html:
                continue

            tbody = client.parseDOM(result_html, 'tbody')
            if not tbody or len(tbody) < 2:
                continue
            self._debug_it('get_sources_packs: parsing done')

            name_info = source_utils.info_from_name(name, self.title, self.year, season=self.season_x, pack=package)
            if source_utils.remove_lang(name_info, self.check_foreign_audio):
                continue
            if self.undesirables and source_utils.remove_undesirables(name_info, self.undesirables):
                continue

            self._debug_it('get_sources_packs: name_info=%s' % name_info)

            seeders, dsize, isize, quality, info = 0, 0, 0, '', ''
            detail = client.parseDOM(tbody[1], 'tr')
            if len(detail) < 2:
                continue
            try:
                seeders = int(re.findall('"retourSeeds">(.*?)</font>', detail[0])[0])
            except:
                seeders = 0

            quality, info = source_utils.get_release_quality(name_info, None)
            try:
                dsize, isize = source_utils._size(re.findall('<strong>(.*?)</strong>', detail[2])[0])
                info.insert(0, isize)
            except:
                dsize = 0
                info = ' | '.join(info)

            but_magnet = re.findall('href=\"(magnet.*?)\"', result_html)
            if not but_magnet:
                continue
            but_magnet = but_magnet[0]

            hash_magnet = re.findall('xt=urn:btih:(.*?)&tr', but_magnet)
            if not hash_magnet:
                continue
            hash_magnet = hash_magnet[0]

            self._debug_it('magnet=%s' % but_magnet)
            self._debug_it('Len=%s  hash=%s' % (len(hash_magnet), hash_magnet))

            if len(hash_magnet) == 32:
                try:
                    hash40 = source_utils.base32_to_hex(hash_magnet, 'get_sources')
                except:
                    continue
            else:
                hash40 = hash_magnet

            self._debug_it('Len=%s  hash40=%s' % (len(hash40), hash40))
            but_magnet_link = 'magnet:?xt=urn:btih:%s' % hash40

            item = {'provider': 'zetorrents', 'source': 'torrent', 'seeders': seeders, 'hash': hash40, 'name': name,
                    'name_info': name_info, 'quality': quality,
                    'language': 'fr', 'url': but_magnet_link, 'info': info, 'direct': False, 'debridonly': True,
                    'size': dsize,
                    'package': package}

            self._debug_it('APPEND PACKS name=%s' % name)
            self._debug_it('APPEND PACKS magnet=%s' % but_magnet_link)
            self._debug_it('APPEND PACKS seeders= %s hash= %s name= %s nameInfo= %s quality= %s size=%s url= %s' % (
                seeders, hash40, name, name_info, quality, isize, but_magnet_link))
            self._debug_it('-')

            if self.search_series:
                item.update({'last_season': last_season})

            elif episode_start:
                item.update({'episode_start': episode_start, 'episode_end': episode_end})  # for partial season packs

            self.sources_append(item)

    def main(self):
        from the_milk.modules.test_modules import Tests
        tests = Tests()
        #self.sources(tests.data_movie_1(), '')
        #self.sources(tests.data_movie_2(), '')
        #self.sources(tests.data_movie_3(), '')
        self.sources(tests.data_movie_4(), '')
        #self.sources(tests.data_serie_1(), '')
        #self.sources(tests.data_serie_2(), '')

        #self.sources_packs(tests.data_serie_packs_1(), '')
        #self.sources_packs(tests.data_serie_packs_2(), '')

if __name__ == "__main__":
    ze = source()
    ze.main()
