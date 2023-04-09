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

        self.base_link = 'https://www.gktorrents.cc'
        self.search_link = '/recherche'
        self.films_link = '/torrents/films'
        self.series_link = '/torrents/series'
        self.min_seeders = 0
        self.debug = False
        self._debug_it('Init')

    def _debug_it(self, msg, caller=None):
        if self.debug:
            log_utils.log('gkTORRENTS | %s' % msg, caller, 1)

    def sources(self, data, host_dict):
        self.sources = []
        if not data:
            self._debug_it('sources: no data')
            return self.sources

        self.sources_append = self.sources.append
        try:
            self.aliases = data['aliases']
            self.year = data['year']
            self.years = []
            if 'tvshowtitle' in data:
                l_title = data['tvshowtitle'].lower().replace('&', 'and').replace('/', '-').replace('$', 's')
                self.title = normalize(l_title)
                self.episode_title = data['title'].lower()
                self.is_movie = False
                self.hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode']))
            else:
                l_title = data['title'].lower().replace('&', 'and').replace('/', '-').replace('$', 's').replace(':', '')
                self.title = normalize(l_title)
                self.episode_title = None
                self.is_movie = True
                self.hdlr = self.year
                self.years = [str(int(self.year) - 1), str(self.year), str(int(self.year) + 1)]

            query = '%s %s' % (l_title, self.hdlr)
            link = '%s%s/%s' % (self.base_link, self.search_link, quote_plus(query))

            self._debug_it('NT=%s T=%s Y=%s H=%s A=%s' % (l_title, self.title, self.year, self.hdlr, self.aliases))
            self._debug_it('link=%s' % link)

            self.undesirables = source_utils.get_undesirables()
            self.check_foreign_audio = source_utils.check_foreign_audio()

            threads = []
            append = threads.append
            append(workers.Thread(self.get_sources, link))

            [i.start() for i in threads]
            [i.join() for i in threads]
            return self.sources
        except Exception as e:
            log_utils.error('sources: %s' % str(e))
            return self.sources

    def get_sources(self, link):
        link = re.sub(r'[\n\t]', '', link)
        if not link:
            return

        try:
            results = client.request(link, timeout=5)
        except Exception as e:
            log_utils.error('Exception on https request search item %s' % str(e))
            return

        if not results or '<tbody' not in results:
            return
        self._debug_it('Request link done link=%s' % link)

        table = client.parseDOM(results, 'tbody')
        if not table or len(table) == 0:
            return
        table = table[0]

        rows = client.parseDOM(table, 'tr')
        if not rows:
            return
        self._debug_it('tr parsing done rows=%s' % len(rows))

        for row in rows:
            if 'Pas de torrents disponibles correspondant à votre recherche' in row:
                continue
            name = re.findall('title="(.*?)">', row)
            if not name:
                continue
            name = normalize(name[0]).replace(' en torrent', '').replace('(version longue)', '').replace(
                'version longue', '').replace('extended', '').replace('amzn', '')

            url = re.findall('href="(.*?)"', row)
            if not url:
                continue
            url = url[0]

            year_str = None
            t = re.split('french|vostfr|truefrench|multi|vff|vfq', name, 1)
            if not t or len(t) < 2:
                continue

            year_str = re.findall("19\d\d|20\d\d", t[1])
            if year_str:
                file_title = str(t[0]) + str(year_str[0])
            else:
                file_title = str(t[0])

            self._debug_it('T=%s N=%s H=%s' % (self.title, file_title, self.hdlr))

            if not source_utils.check_title(self.title, self.aliases, file_title, self.hdlr, self.year, self.years):
                self._debug_it('check_title FAILED!  T=%s N=%s H=%s Y=%s YS=%s' % (
                    self.title, file_title, self.hdlr, self.year, self.years))
                continue
            self._debug_it('check_title OK!  T=%s N=%s Y=%s' % (self.title, file_title, self.year))

            link = '%s%s' % (self.base_link, url)
            self._debug_it('link=%s' % link)

            try:
                result_html = client.request(link, timeout=5)
            except Exception as e:
                log_utils.error('Exception https request page infos %s' % str(e))
                continue

            if not result_html or 'magnet:?xt=urn:btih:' not in result_html:
                continue

            tbody = client.parseDOM(result_html, 'tbody')
            if not tbody or len(tbody) < 2:
                continue
            self._debug_it('parsing done')

            name_info = source_utils.info_from_name(name, self.title, self.year, self.hdlr, self.episode_title)
            self._debug_it('name_info=%s' % name_info)

            if source_utils.remove_lang(name_info, self.check_foreign_audio):
                continue
            if self.undesirables and source_utils.remove_undesirables(name_info, self.undesirables):
                continue

            seeders, dsize, isize, quality, info = 0, 0, 0, '', ''
            detail = client.parseDOM(tbody[1], 'tr')
            if len(detail) < 5:
                continue
            try:
                seeders = int(re.findall('"retourSeeds">(.*?)</font>', detail[3])[0])
            except Exception as e:
                seeders = 0

            self._debug_it('seeders=%s' % seeders)
            quality, info = source_utils.get_release_quality(name_info, None)
            try:
                dsize, isize = source_utils._size(re.findall('<strong>(.*?)</strong>', detail[2])[0])
                info.insert(0, isize)
            except Exception as e:
                log_utils.error('source_utils._size failed! %s' % str(e))
                dsize = 0
                info = ' | '.join(info)

            self._debug_it('dsize=%s isize=%s' % (dsize, isize))
            but_magnet = re.findall('href=\'(magnet.*?)\'', result_html)
            if not but_magnet:
                continue
            but_magnet = but_magnet[0]

            hash_magnet = re.findall('xt=urn:btih:(.*?)&tr', but_magnet)
            if not hash_magnet:
                continue
            hash_magnet = hash_magnet[0]
            if len(hash_magnet) < 32:
                continue

            self._debug_it('magnet=%s' % but_magnet)
            self._debug_it('Len=%s  hash=%s' % (len(hash_magnet), hash_magnet))

            if len(hash_magnet) == 32:
                try:
                    hash40 = source_utils.base32_to_hex(hash_magnet, 'get_sources')
                except Exception as e:
                    log_utils.error('source_utils.base32_to_hex failed! %s' % str(e))
                    continue
            else:
                hash40 = hash_magnet

            self._debug_it('Len=%s  hash40=%s' % (len(hash40), hash40))
            but_magnet_link = 'magnet:?xt=urn:btih:%s' % hash40

            self.sources_append(
                {'provider': 'gktorrents', 'source': 'torrent', 'seeders': seeders, 'hash': hash40, 'name': name,
                 'name_info': name_info,
                 'quality': quality, 'language': 'fr', 'url': but_magnet_link, 'info': info, 'direct': False,
                 'debridonly': True,
                 'size': dsize})

            self._debug_it('APPEND name=%s' % name)
            self._debug_it('APPEND magnet=%s' % but_magnet_link)
            self._debug_it('APPEND seeders= %s hash= %s name= %s nameInfo= %s quality= %s size=%s url= %s' % (
                seeders, hash40, name, name_info, quality, isize, but_magnet_link))
            self._debug_it('-')

    def sources_packs(self, data, host_dict, search_series=False, total_seasons=None, bypass_filter=False):
        self.sources = []
        if not data:
            return self.sources

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
            log_utils.error('sources_pack Exception %s' % str(e))
            return self.sources

    def get_sources_packs(self, season_url):
        if not season_url:
            return
        self._debug_it('Season url=%s' % season_url)

        link = re.sub(r'[\n\t]', '', season_url)
        if not link:
            return

        try:
            results = client.request(link, timeout=5)
        except Exception as e:
            log_utils.error('https request search Pack items %s' % str(e))
            return
        if not results or '<tbody' not in results:
            return

        table = client.parseDOM(results, 'tbody')
        if not table:
            return
        table = table[0]
        rows = client.parseDOM(table, 'tr')
        if not rows:
            return
        self._debug_it('tr parsing done rows=%s' % len(rows))

        for row in rows:
            if 'Pas de torrents disponibles correspondant à votre recherche' in row:
                continue
            name = re.findall('title="(.*?)">', row)
            if not name:
                continue
            name = normalize(name[0]).replace(' en torrent', '').replace('amzn', '')

            url = re.findall('href="(.*?)"', row)
            if not url:
                continue
            url = url[0]

            year_name = None
            t = re.split('french|vostfr|truefrench|multi|vff|vfq', name, 1)
            if not t or len(t) < 2:
                continue

            year_name = re.findall("19\d\d|20\d\d", t[1])
            if year_name:
                file_title = str(t[0]) + str(year_name[0])
            else:
                file_title = str(t[0])

            self._debug_it('T=%s N=%s' % (self.title, file_title))

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

            link = '%s%s' % (self.base_link, url)
            try:
                result_html = client.request(link, timeout=5)
            except Exception as e:
                log_utils.error('https request page Pack infos %s' % str(e))
                continue

            if not result_html or 'magnet:?xt=urn:btih:' not in result_html:
                continue

            tbody = client.parseDOM(result_html, 'tbody')
            if not tbody or len(tbody) < 2: continue
            self._debug_it('parsing done')

            name_info = source_utils.info_from_name(name, self.title, self.year, season=self.season_x, pack=package)
            self._debug_it('name_info=%s' % name_info)

            if source_utils.remove_lang(name_info, self.check_foreign_audio):
                continue
            if self.undesirables and source_utils.remove_undesirables(name_info, self.undesirables):
                continue

            seeders, dsize, isize, quality, info = 0, 0, 0, '', ''
            detail = client.parseDOM(tbody[1], 'tr')
            if len(detail) < 5:
                continue

            try:
                seeders = int(re.findall('"retourSeeds">(.*?)</font>', detail[3])[0])
            except Exception as e:
                log_utils.error('re.findall failed! %s' % str(e))
                seeders = 0

            quality, info = source_utils.get_release_quality(name_info, None)
            try:
                dsize, isize = source_utils._size(re.findall('<strong>(.*?)</strong>', detail[2])[0])
                info.insert(0, isize)
            except Exception as e:
                log_utils.error('source_utils._size failed! %s' % str(e))
                dsize = 0
                info = ' | '.join(info)

            but_magnet = re.findall('href=\'(magnet.*?)\'', result_html)
            if not but_magnet:
                continue
            but_magnet = but_magnet[0]

            hash_magnet = re.findall('xt=urn:btih:(.*?)&tr', but_magnet)
            if not hash_magnet:
                continue
            hash_magnet = hash_magnet[0]
            if len(hash_magnet) < 32:
                continue

            self._debug_it('magnet=%s' % but_magnet)
            self._debug_it('Len=%s  hash=%s' % (len(hash_magnet), hash_magnet))

            if len(hash_magnet) == 32:
                try:
                    hash40 = source_utils.base32_to_hex(hash_magnet, 'get_sources')
                except Exception as e:
                    log_utils.error('source_utils.base32_to_hex failed! %s' % str(e))
                    continue
            else:
                hash40 = hash_magnet

            self._debug_it('Len=%s  hash40=%s' % (len(hash40), hash40))
            but_magnet_link = 'magnet:?xt=urn:btih:%s' % hash40
            item = {'provider': 'gktorrents', 'source': 'torrent', 'seeders': seeders, 'hash': hash40, 'name': name,
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
        self.sources(Tests.data_movie_1, '')
        self.sources(Tests.data_serie_1, '')
        self.sources(Tests.data_serie_2, '')

        self.sources_packs(Tests.data_serie_packs_1, '')
        self.sources_packs(Tests.data_serie_packs_2, '')

if __name__ == "__main__":
    tgk = source()
    tgk.main()
