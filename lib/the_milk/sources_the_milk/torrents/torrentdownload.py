# -*- coding: utf-8 -*-
# created by Venom for Fenomscrapers (updated 7-19-2022)
"""
	Fenomscrapers Project
"""

import re
from urllib.parse import quote_plus, unquote_plus
from the_milk.modules import client
from the_milk.modules import source_utils
from the_milk.modules import workers


class source:
    priority = 3
    pack_capable = True
    has_movies = True
    has_episodes = True

    def __init__(self):
        self.language = ['en']
        self.base_link = "https://www.torrentdownload.info"
        self.search_link = '/search?q=%s'
        self.min_seeders = 0

    def sources(self, data, host_dict):
        self.sources = []
        if not data: return self.sources
        self.sources_append = self.sources.append
        try:
            self.aliases = data['aliases']
            self.year = data['year']
            if 'tvshowtitle' in data:
                self.title = data['tvshowtitle'].replace('&', 'and').replace('Special Victims Unit', 'SVU').replace('/',
                                                                                                                    ' ').replace(
                    '$', 's')
                self.episode_title = data['title']
                self.hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode']))
            else:
                self.title = data['title'].replace('&', 'and').replace('/', ' ').replace('$', 's')
                self.episode_title = None
                self.hdlr = self.year
            query = '%s %s' % (re.sub(r'[^A-Za-z0-9\s\.-]+', '', self.title), self.hdlr)
            urls = []
            url = '%s%s' % (self.base_link, self.search_link % quote_plus(query))
            urls.append(url)
            urls.append(url + '&p=2')
            # log_utils.log('urls = %s' % urls)
            self.undesirables = source_utils.get_undesirables()
            self.check_foreign_audio = source_utils.check_foreign_audio()
            threads = []
            append = threads.append
            for url in urls:
                append(workers.Thread(self.get_sources, url))
            [i.start() for i in threads]
            [i.join() for i in threads]
            return self.sources
        except:
            source_utils.scraper_error('TORRENTDOWNLOAD')
            return self.sources

    def get_sources(self, url):
        try:
            results = client.request(url, timeout=5)
            if not results: return
            rows = client.parseDOM(results, 'tr')
        except:
            source_utils.scraper_error('TORRENTDOWNLOAD')
            return

        for row in rows:
            try:
                if any(value in row for value in ('<th', 'nofollow')): continue
                columns = re.findall(r'<td.*?>(.+?)</td>', row, re.DOTALL)

                link = re.search(r'href\s*=\s*["\']/(.+?)["\']>', columns[0], re.I).group(1).split('/')
                hash = link[0]
                name = source_utils.clean_name(unquote_plus(link[1]).replace('&amp;', '&'))

                if not source_utils.check_title(self.title, self.aliases, name, self.hdlr, self.year): continue
                name_info = source_utils.info_from_name(name, self.title, self.year, self.hdlr, self.episode_title)
                if source_utils.remove_lang(name_info, self.check_foreign_audio): continue
                if self.undesirables and source_utils.remove_undesirables(name_info, self.undesirables): continue

                if not self.episode_title:  # filter for eps returned in movie query (rare but movie and show exists for Run in 2020)
                    ep_strings = [r'[.-]s\d{2}e\d{2}([.-]?)', r'[.-]s\d{2}([.-]?)', r'[.-]season[.-]?\d{1,2}[.-]?']
                    name_lower = name.lower()
                    if any(re.search(item, name_lower) for item in ep_strings): continue

                url = 'magnet:?xt=urn:btih:%s&dn=%s' % (hash, name)
                try:
                    seeders = int(columns[3].replace(',', ''))
                    if self.min_seeders > seeders: continue
                except:
                    seeders = 0

                quality, info = source_utils.get_release_quality(name_info, url)
                try:
                    dsize, isize = source_utils._size(columns[2])
                    info.insert(0, isize)
                except:
                    dsize = 0
                info = ' | '.join(info)

                self.sources_append(
                    {'provider': 'torrentdownload', 'source': 'torrent', 'seeders': seeders, 'hash': hash, 'name': name,
                     'name_info': name_info,
                     'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False,
                     'debridonly': True, 'size': dsize})
            except:
                source_utils.scraper_error('TORRENTDOWNLOAD')

    def sources_packs(self, data, host_dict, search_series=False, total_seasons=None, bypass_filter=False):
        self.sources = []
        if not data: return self.sources
        self.sources_append = self.sources.append
        try:
            self.search_series = search_series
            self.total_seasons = total_seasons
            self.bypass_filter = bypass_filter

            self.title = data['tvshowtitle'].replace('&', 'and').replace('Special Victims Unit', 'SVU').replace('/',
                                                                                                                ' ').replace(
                '$', 's')
            self.aliases = data['aliases']
            self.imdb = data['imdb']
            self.year = data['year']
            self.season_x = data['season']
            self.season_xx = self.season_x.zfill(2)
            self.undesirables = source_utils.get_undesirables()
            self.check_foreign_audio = source_utils.check_foreign_audio()

            query = re.sub(r'[^A-Za-z0-9\s\.-]+', '', self.title)
            if search_series:
                queries = [
                    self.search_link % quote_plus(query + ' Season'),
                    self.search_link % quote_plus(query + ' Complete')]
            else:
                queries = [
                    self.search_link % quote_plus(query + ' S%s' % self.season_xx),
                    self.search_link % quote_plus(query + ' Season %s' % self.season_x)]
            threads = []
            append = threads.append
            for url in queries:
                link = '%s%s' % (self.base_link, url)
                append(workers.Thread(self.get_sources_packs, link))
            [i.start() for i in threads]
            [i.join() for i in threads]
            return self.sources
        except:
            source_utils.scraper_error('TORRENTDOWNLOAD')
            return self.sources

    def get_sources_packs(self, link):
        try:
            results = client.request(link, timeout=5)
            if not results: return
            rows = client.parseDOM(results, 'tr')
        except:
            source_utils.scraper_error('TORRENTDOWNLOAD')
            return

        for row in rows:
            try:
                if any(value in row for value in ('<th', 'nofollow')): continue
                columns = re.findall(r'<td.*?>(.+?)</td>', row, re.DOTALL)

                link = re.search(r'href\s*=\s*["\']/(.+?)["\']>', columns[0], re.I).group(1).split('/')
                hash = link[0]
                name = source_utils.clean_name(unquote_plus(link[1]).replace('&amp;', '&'))

                episode_start, episode_end = 0, 0
                if not self.search_series:
                    if not self.bypass_filter:
                        valid, episode_start, episode_end = source_utils.filter_season_pack(self.title, self.aliases,
                                                                                            self.year, self.season_x,
                                                                                            name)
                        if not valid: continue
                    package = 'season'

                elif self.search_series:
                    if not self.bypass_filter:
                        valid, last_season = source_utils.filter_show_pack(self.title, self.aliases, self.imdb,
                                                                           self.year, self.season_x, name,
                                                                           self.total_seasons)
                        if not valid: continue
                    else:
                        last_season = self.total_seasons
                    package = 'show'

                name_info = source_utils.info_from_name(name, self.title, self.year, season=self.season_x, pack=package)
                if source_utils.remove_lang(name_info, self.check_foreign_audio): continue
                if self.undesirables and source_utils.remove_undesirables(name_info, self.undesirables): continue

                url = 'magnet:?xt=urn:btih:%s&dn=%s' % (hash, name)
                try:
                    seeders = int(columns[3].replace(',', ''))
                    if self.min_seeders > seeders: continue
                except:
                    seeders = 0

                quality, info = source_utils.get_release_quality(name_info, url)
                try:
                    dsize, isize = source_utils._size(columns[2])
                    info.insert(0, isize)
                except:
                    dsize = 0
                info = ' | '.join(info)

                item = {'provider': 'torrentdownload', 'source': 'torrent', 'seeders': seeders, 'hash': hash,
                        'name': name, 'name_info': name_info, 'quality': quality,
                        'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True, 'size': dsize,
                        'package': package}
                if self.search_series:
                    item.update({'last_season': last_season})
                elif episode_start:
                    item.update(
                        {'episode_start': episode_start, 'episode_end': episode_end})  # for partial season packs
                self.sources_append(item)
            except:
                source_utils.scraper_error('TORRENTDOWNLOAD')
