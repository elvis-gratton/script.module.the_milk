# -*- coding: utf-8 -*-
# Fork of Projects from Venom Fenomscrapers, TikiPeter FEN, CocoJoe2411 cocoscrapers
# French Torrent yggtorrent.do

import re
from enum import Enum
from urllib.parse import quote_plus
from the_milk.modules import client
from the_milk.modules import source_utils
from the_milk.modules import workers
from the_milk.modules import log_utils
from the_milk.modules.cleantitle import normalize
# import web_pdb



class source:
    priority = 5
    pack_capable = True
    has_movies = True
    has_episodes = True


    class _subcats(Enum):
        ALL = '&sub_category=all'
        ANIMATION = '&sub_category=2178'
        SERIE_ANIMATION = '&sub_category=2179'
        CONCERT = '&sub_category=2180'
        DOCU = '&sub_category=2181'
        EMISSION_TV = '&sub_category=2182'
        FILM = '&sub_category=2183'
        SERIE_TV = '&sub_category=2184'
        SPECTACLE = '&sub_category=2185'
        SPORT = '&sub_category=2186'
        VIDEO_CLIP = '&sub_category=2187'


    def __init__(self):
        self.language = ['fr']
        self.base_link = 'https://www3.yggtorrent.wtf/engine/search?category=2145'  # film/video
        self.min_seeders = 0
        self.debug = False
        self._debug_it('Init')

    def _debug_it(self, msg, caller=None):
        if self.debug:
            log_utils.log('yggTorrent | %s' % msg, caller, 1)

    def _is_genre_present(self, search, genres):
        """
        !!! language fr-fr or en-US... alter search word in list
        :param search:  str 'comedie','docu'...
        :param genres:  list of str
        :return: boolean
        """
        if search and len(search) > 0 and genres and len(genres) > 0:
            if search in genres:
                return True
            else:
                return False
        else:
            return False

    def _option_saison(self, season_id: int):
        """
        :param season_id:  int 1..30
        :return: ex: &option_saison[]=4..9..14
        """
        c_option_season = '&option_saison[]=%s'
        response = ''
        if season_id in range(1, 30):
            response = c_option_season % str(season_id + 3)     # offset 3
        else:
            log_utils.error('yggTorrent._option_saison: params not in range (1..30)')
        return response

    def _option_episode(self, episode_id: int):
        """
        :param episode_id:  int 1..60
        :return:    str '&option_episode[]=4'...
        """
        c_option_episode = '&option_episode[]=%s'
        response = ''
        if episode_id in range(1, 60):
            response = c_option_episode % str(episode_id + 1)   # offset 1
        else:
            log_utils.error('yggTorrent._option_episode: params not in range (1..60)')
        return response

    def _create_link(self, title, cat=_subcats.ALL, integrale=False, season=None, episode=None):
        """
        :param title:   string of movie or serie
        :param cat:     enum of sub category
        :param integrale: Boolean Integrale=True
        :param season:  str 1..30 or None
        :param episode: str 1..60 or None
        :return:        str '&option_saison[]=4&option_episode[]=1'
        """
        url = ''
        if not title or len(title) == 0:
            return url

        if season and type(season) != str:
            log_utils.error('yggTorrent._create_link: bad param season not str')
            return url
        if episode and type(episode) != str:
            log_utils.error('yggTorrent._create_link: bad param episode not str')
            return url

        search_title = '&do=search&name=%s' % title
        opt_season, opt_episode, cintegrale = '', '', '&option_saison[]=1'

        if cat is self._subcats.ALL:
            url = self.base_link + self._subcats.ALL.value + search_title

        elif cat is self._subcats.FILM:
            url = self.base_link + self._subcats.FILM.value + search_title

        elif cat is self._subcats.DOCU:
            url = self.base_link + self._subcats.DOCU.value + search_title

        elif cat is self._subcats.CONCERT:
            url = self.base_link + self._subcats.CONCERT.value + search_title

        elif cat is self._subcats.SPECTACLE:
            url = self.base_link + self._subcats.SPECTACLE.value + search_title

        elif cat is self._subcats.ANIMATION:
            url = self.base_link + self._subcats.ANIMATION.value + search_title

        elif cat is self._subcats.VIDEO_CLIP:
            url = self.base_link + self._subcats.VIDEO_CLIP.value + search_title

        elif cat is self._subcats.SERIE_TV:
            if integrale:
                opt_season = cintegrale
            else:
                if season:
                    try:
                        opt_season = self._option_saison(int(season))
                    except ValueError as ve:
                        log_utils.error('yggTorrent._create_link: Exception SERIE_TV bad param season int(season) %s' % str(ve))

                if episode:
                    try:
                        opt_episode = self._option_episode(int(episode))
                    except ValueError as ve:
                        log_utils.error('yggTorrent._create_link: Exception SERIE_TV bad param episode int(episode) %s' % str(ve))

            url = self.base_link + self._subcats.SERIE_TV.value + opt_season + opt_episode + search_title

        elif cat is self._subcats.SERIE_ANIMATION:
            if integrale:
                opt_season = cintegrale
            else:
                if season:
                    try:
                        opt_season = self._option_saison(int(season))
                    except ValueError as ve:
                        log_utils.error('yggTorrent._create_link: Exception SERIE_ANIMATION bad param season int(season) %s' % str(ve))

                if episode:
                    try:
                        opt_episode = self._option_episode(int(episode))
                    except ValueError as ve:
                        log_utils.error('yggTorrent._create_link: Exception SERIE_ANIMATION bad param episode int(episode) %s' % str(ve))

            url = self.base_link + self._subcats.SERIE_ANIMATION.value + opt_season + opt_episode + search_title

        elif cat is self._subcats.EMISSION_TV:
            if integrale:
                opt_season = cintegrale
            else:
                if season:
                    try:
                        opt_season = self._option_saison(int(season))
                    except ValueError as ve:
                        log_utils.error('yggTorrent._create_link: Exception EMISSION_TV bad param season int(season) %s' % str(ve))

                if episode:
                    try:
                        opt_episode = self._option_episode(int(episode))
                    except ValueError as ve:
                        log_utils.error('yggTorrent._create_link: Exception EMISSION_TV bad param episode int(episode) %s' % str(ve))

            url = self.base_link + self._subcats.EMISSION_TV.value + opt_season + opt_episode + search_title
        else:
            pass
        return quote_plus(url, ':/?&=')

    def _film_serie_link(self, l_title, flag_movie=True, genres=[], integrale=False, l_season=None, l_episode=None):
        """
        :param l_title:     title name of movie serie
        :param flag_movie:  boolean movie/serie
        :param genres:      list of string
        :param integrale:   boolean integrale=True
        :param l_season:    str 1..30
        :param l_episode:   str 1..60
        :return:    str url of request search
        """
        url = ''
        if not l_title or len(l_title) == 0:
            self._debug_it('_film_serie_link:  error l_title param')
            return url

        if flag_movie:
            if self._is_genre_present('animation', genres):
                url = self._create_link(l_title, self._subcats.ANIMATION)

            elif self._is_genre_present('docu', genres):
                url = self._create_link(l_title, self._subcats.DOCU)

            else:
                url = self._create_link(l_title, self._subcats.FILM)

        else:
            if self._is_genre_present('animation', genres):
                url = self._create_link(l_title, self._subcats.SERIE_ANIMATION, integrale, l_season, l_episode)

            elif self._is_genre_present('docu', genres):
                if integrale:
                    url = self._create_link(l_title, self._subcats.EMISSION_TV, integrale)
                else:
                    tmp = '+S%02d' % int(l_season)
                    url = self._create_link(l_title, self._subcats.ALL) + tmp

            else:
                url = self._create_link(l_title, self._subcats.SERIE_TV, integrale, l_season, l_episode)

        return url

    def sources(self, data, host_dict):
        """
        :param data:
        :param host_dict:
        :return:
        """
        self.sources = []
        if not data:
            log_utils.error('yggTorrent.sources: data empty')
            return self.sources

        self.sources_append = self.sources.append
        try:
            self.aliases = data['aliases']
            self.original_title = data['original_title'].lower()
            genres = data.get('genre')

            if 'tvshowtitle' in data:
                l_title = data['tvshowtitle'].lower().replace('/', '-').replace('$', 's').replace('!', '')
                self.title = normalize(l_title)
                self.episode_title = data['title'].lower()
                self.is_movie = False
                self.year = ''
                self.hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode']))
                season = data['season']
                episode = data['episode']
                self.years = None
            else:
                l_title = data['title'].lower().replace('/', '-').replace('$', 's').replace('!', '')
                self.title = normalize(l_title)
                self.episode_title = None
                self.is_movie = True
                self.year = data['year']
                self.hdlr = self.year
                season = None
                episode = None
                try:
                    self.years = [str(int(self.year) - 1), self.year, str(int(self.year) + 1)]
                except:
                    self.years = None

            t = self.title.replace(' ', '')
            ot = normalize(self.original_title).replace(' ', '').replace('!', '')
            if t == ot:
                title_equal = True
            else:
                title_equal = False

            self._debug_it('sources: Y=%s H=%s A=%s' % (self.year, self.hdlr, self.aliases))
            self._debug_it('sources: isEqual=%s title=%s original_title=%s' % (title_equal, t, ot))

            links = []
            # with title
            link = self._film_serie_link(l_title, self.is_movie, genres, False, season, episode)

            if self.is_movie:
                links.append(link + '+%s' % self.years[0])  # movie only with year - 1
                links.append(link + '+%s' % self.years[1])  # movie only with year
                links.append(link + '+%s' % self.years[2])  # movie only with year + 1
            else:
                links.append(link)  # without year

            # with original_title
            if not title_equal:
                link = self._film_serie_link(self.original_title, self.is_movie, genres, False, season, episode)
                if self.is_movie:
                    links.append(link + '+%s' % self.years[0])  # movie only with year - 1
                    links.append(link + '+%s' % self.years[1])  # movie only with year
                    links.append(link + '+%s' % self.years[2])  # movie only with year + 1
                else:
                    links.append(link)  # without year


            self._debug_it('sources: links=%s' % links)

            self.undesirables = source_utils.get_undesirables()
            threads = []
            append = threads.append

            for link in links:
                append(workers.Thread(self.get_sources, link))

            [i.start() for i in threads]
            [i.join() for i in threads]
            return self.sources
        except Exception as e:
            log_utils.error('yggTorrent.sources: %s' % str(e))
            return self.sources

    def get_sources(self, link):
        """
        :param link:
        :return:
        """

        if 'https:' not in link:
            return None
        link = re.sub(r'[\n\t]', '', link)


        # https Request 1. Search Page
        try:
            results = client.request(link, timeout=5)
        except Exception as e:
            log_utils.error('YggTorrent.get_sources: Exception https request search item %s' % str(e))
            return None

        if not results or 'Aucun résultat !' in results:
            self._debug_it('get_sources: link = %s' % link)
            self._debug_it('get_sources: Aucun résultat !')
            return  None

        if '<tbody' not in results:
            return None

        table = client.parseDOM(results, 'tbody')
        if not table or len(table) < 2:
            return  None
        table = table[1]

        rows = client.parseDOM(table, 'tr')
        if not rows:
            return  None
        self._debug_it('get_sources: tr parsing done rows=%s' % len(rows))
        self._debug_it('-')

        for row in rows:

            td = client.parseDOM(row, 'td')
            if not td or len(td) < 2:
                continue

            part = td[1].split('">')
            if len(part) < 2 or len(part[1]) == 0:
                continue

            if 'href="https://' in part[0]:
                url = part[0].split('href="')[1]
                url = quote_plus(url, ':/?&=')
            else:
                continue

            filename = normalize(part[1]).replace('version longue', '').replace('extended', '').replace('complete', '').replace('integrale', '')
            if 'vostfr' in filename or 'vost.en-fr' in filename or 'subfrench' in filename or 'cfemail' in filename:
                continue

            year_str = re.findall("19\d\d|20\d\d", filename)
            if year_str:
                year_str = year_str[0]

            name_info = source_utils.info_from_name(filename, self.title, self.year, self.hdlr, self.episode_title)
            self._debug_it('get_sources: name_info=%s' % name_info)

            if not self.is_movie:
                tmp_filename = re.sub(".19\d\d|.20\d\d", '', filename)
            else:
                tmp_filename = filename

            if not source_utils.check_title(self.title, self.aliases, tmp_filename, self.hdlr, self.year, self.years):
                if not source_utils.check_title(self.original_title, self.aliases, tmp_filename, self.hdlr, self.year, self.years):
                    self._debug_it('get_sources: check_title FAILED!  T=%s OT=%s FN=%s H=%s Y=%s YS=%s' % (self.title, self.original_title, filename, self.hdlr, self.year, self.years))
                    continue

            self._debug_it('get_sources: check_title OK!  T=%s FT=%s Y=%s A=%s' % (self.title, filename, self.year, self.aliases))

            ### https Request 2. Page Infos ###
            try:
                result_html = client.request(url, timeout=5)
            except Exception as e:
                log_utils.error('YggTorrent.get_sources: Exception https request page infos %s' % str(e))
                continue

            if not result_html or '<td>Info Hash</td>' not in result_html:
                self._debug_it('get_sources: info_hash not present!')
                continue
            else:
                self._debug_it('get_sources: infoHash found!')

            tbody = client.parseDOM(result_html, 'tbody')
            if not tbody or len(tbody) < 2:
                continue

            seeders, dsize, isize, quality, info = 0, 0, 0, '', ''
            tr = client.parseDOM(tbody[0], 'tr')
            if len(tr) < 2:
                continue
            try:
                seeders = int(re.findall('<td><strong class="green">(.*?)</strong></td>', tr[2])[0])
            except:
                seeders = 0

            quality, info = source_utils.get_release_quality(name_info, None)
            trx = client.parseDOM(tbody[1], 'tr')
            if len(trx) < 2:
                continue

            try:
                dsize, isize = source_utils._size(re.findall('<td>(.*?)</td>', trx[3])[1])
                info.insert(0, isize)
            except:
                dsize = 0
                info = ' | '.join(info)

            try:
                info_hash = re.findall('<td>(.*?)</td>', trx[4])[1]
            except:
                continue

            self._debug_it('get_sources: parsing done')

            if len(info_hash) == 32:
                try:
                    hash40 = source_utils.base32_to_hex(info_hash, 'get_sources')
                except Exception as e:
                    self._debug_it('get_sources: base32_to_hex %s' % str(e))
                    continue
            else:
                hash40 = info_hash
            but_magnet_link = 'magnet:?xt=urn:btih:%s' % hash40

            self.sources_append(
                {'provider': 'yggtorrent', 'source': 'torrent', 'seeders': seeders, 'hash': hash40, 'name': filename,
                 'name_info': name_info, 'quality': quality, 'language': 'fr', 'url': but_magnet_link, 'info': info, 'direct': False,
                 'debridonly': True, 'size': dsize})

            self._debug_it('APPEND filename= %s' % filename)
            self._debug_it('APPEND quality= %s size= %s' % (quality, isize))
            self._debug_it('APPEND magnet= %s' % but_magnet_link)
            self._debug_it(
                'APPEND seeders= %s hash= %s filename= %s nameInfo= %s quality= %s size=%s url= %s' % (
                    seeders, hash40, filename, name_info, quality, isize, but_magnet_link))
            self._debug_it('-')

    def sources_packs(self, data, host_dict, search_series=False, total_seasons=None, bypass_filter=False):
        """
        :param data:
        :param host_dict:
        :param search_series:
        :param total_seasons:
        :param bypass_filter:
        :return:
        """
        self.sources = []
        if not data:
            log_utils.error('yggTorrent.sources_packs: data empty')
            return self.sources

        self._debug_it('sources_packs')
        self.sources_append = self.sources.append
        genres = data['genre']
        self.original_title = data['original_title'].lower()

        try:
            self.search_series = search_series
            self.total_seasons = total_seasons
            self.bypass_filter = bypass_filter

            l_title = data['tvshowtitle'].lower().replace('/', ' ').replace('$', 's').replace('!', '')   # metadata name, ep_name ex: S01E01
            self.title = normalize(l_title)
            self.aliases = data['aliases']
            self.imdb = data['imdb']
            self.year = data['year']
            self.season_x = data['season']
            self.season_xx = self.season_x.zfill(2)
            self.undesirables = source_utils.get_undesirables()
            self.check_foreign_audio = source_utils.check_foreign_audio()

            t = self.title.replace(' ', '')
            ot = normalize(self.original_title).replace(' ', '').replace('!', '')
            if t == ot:
                title_equal = True
            else:
                title_equal = False

            links = []

            self._debug_it('sources_packs: isEqual=%s title=%s original_title=%s' % (title_equal, t, ot))

            # with title
            link = self._film_serie_link(l_title, False, genres, False, data['season'])
            links.append(link)

            # with original_title
            if not title_equal:
                link = self._film_serie_link(self.original_title, False, genres, False, data['season'])
                links.append(link)

            # integrale with title
            link = self._film_serie_link(l_title, False, genres, True)
            links.append(link)

            # integrale with original_title
            if not title_equal:
                link = self._film_serie_link(self.original_title, False, genres, True)
                links.append(link)

            self._debug_it('sources_packs: links= %s' % links)
            threads = []
            append = threads.append

            for link in links:
                append(workers.Thread(self.get_sources_packs, link))

            [i.start() for i in threads]
            [i.join() for i in threads]
            return self.sources

        except Exception as e:
            log_utils.error('YggTorrent.sources_packs: Exception %s' % str(e))
            return self.sources

    def get_sources_packs(self, link):
        """
        :param link:
        :return:
        """
        if 'https:' not in link:
            return None
        link = re.sub(r'[\n\t]', '', link)

        ### https Request 1. Search Page ###
        try:
            results = client.request(link, timeout=5)
        except Exception as e:
            log_utils.error('YggTorrent.get_sources_packs: Exception https request search item %s' % str(e))
            return  None

        if not results or 'Aucun résultat !' in results:
            self._debug_it('get_sources_packs: link = %s' % link)
            self._debug_it('get_sources_packs: Aucun résultat !')
            return  None

        if '<tbody' not in results:
            return  None

        table = client.parseDOM(results, 'tbody')
        if not table or len(table) < 2:
            return  None
        table = table[1]

        rows = client.parseDOM(table, 'tr')
        if not rows:
            return  None
        self._debug_it('get_sources_packs: tr parsing done rows=%s' % len(rows))
        self._debug_it('-')

        for row in rows:

            td = client.parseDOM(row, 'td')
            if not td or len(td) < 2:
                continue

            part = td[1].split('">')
            if len(part) < 2 or len(part[1]) == 0:
                continue

            if 'href="https://' in part[0]:
                url = part[0].split('href="')[1]
                url = quote_plus(url, ':/?&=')
            else:
                continue

            filename = normalize(part[1]).replace('version longue', '').replace('extended', '').replace('integrale', '').replace('integral', '')
            if 'vostfr' in filename or 'vost.en-fr' in filename or 'subfrench' in filename or 'cfemail' in filename:
                continue

            year_str = re.findall("19\d\d|20\d\d", filename)
            if year_str:
                year_str = year_str[0]

            tmp_filename = re.sub(".19\d\d|.20\d\d", '', filename)
            self._debug_it('get_sources_packs: T=%s filename=%s' % (self.title, tmp_filename))

            episode_start, episode_end, valid = 0, 0, False
            if not self.search_series:
                if not self.bypass_filter:
                    valid, episode_start, episode_end = source_utils.filter_season_pack(self.title, self.aliases, self.year, self.season_x, tmp_filename)
                    self._debug_it('get_sources_packs:1. filter season valid=%s' % str(valid))
                    if not valid:
                        valid, episode_start, episode_end = source_utils.filter_season_pack(self.original_title, self.aliases, self.year, self.season_x, tmp_filename)
                        self._debug_it('get_sources_packs:2. filter season valid=%s' % str(valid))
                        if not valid:
                            continue
                package = 'season'

            elif self.search_series:
                if not self.bypass_filter:
                    valid, last_season = source_utils.filter_show_pack(self.title, self.aliases, self.imdb, self.year, self.season_x, tmp_filename, self.total_seasons)
                    self._debug_it('get_sources_packs:1 filter show valid=%s' % str(valid))
                    if not valid:
                        valid, last_season = source_utils.filter_show_pack(self.original_title, self.aliases, self.imdb, self.year, self.season_x, tmp_filename, self.total_seasons)
                        self._debug_it('get_sources_packs:2 filter show valid=%s' % str(valid))
                        if not valid:
                            continue
                else:
                    last_season = self.total_seasons
                package = 'show'


            self._debug_it('get_sources_packs: filter result OK!  T=%s OT=%s FN=%s Y=%s A=%s' % ( self.title,self.original_title, filename, self.year, self.aliases))

            ### https Request 2. Page Infos ###
            try:
                result_html = client.request(url, timeout=5)
            except Exception as e:
                log_utils.error('YggTorrent.get_sources_packs: Exception https request page infos %s' % str(e))
                continue

            if not result_html or '<td>Info Hash</td>' not in result_html:
                continue

            tbody = client.parseDOM(result_html, 'tbody')
            if not tbody or len(tbody) < 2:
                continue

            name_info = source_utils.info_from_name(filename, self.title, self.year, season=self.season_x, pack=package)
            self._debug_it('get_sources_packs: name_info=%s' % name_info)

            seeders, dsize, isize, quality, info = 0, 0, 0, '', ''
            tr = client.parseDOM(tbody[0], 'tr')
            if len(tr) < 2:
                continue
            try:
                seeders = int(re.findall('<td><strong class="green">(.*?)</strong></td>', tr[2])[0])
            except:
                seeders = 0

            quality, info = source_utils.get_release_quality(name_info, None)
            trx = client.parseDOM(tbody[1], 'tr')
            if len(trx) < 2:
                continue

            try:
                dsize, isize = source_utils._size(re.findall('<td>(.*?)</td>', trx[3])[1])
                info.insert(0, isize)
            except:
                dsize = 0
                info = ' | '.join(info)
            try:
                info_hash = re.findall('<td>(.*?)</td>', trx[4])[1]
            except:
                continue

            self._debug_it('get_sources_packs: parsing done')

            if len(info_hash) == 32:
                try:
                    hash40 = source_utils.base32_to_hex(info_hash, 'get_sources')
                except:
                    continue
            else:
                hash40 = info_hash
            but_magnet_link = 'magnet:?xt=urn:btih:%s' % hash40

            item = {'provider': 'yggtorrent', 'source': 'torrent', 'seeders': seeders, 'hash': hash40, 'name': filename,
                    'name_info': name_info, 'quality': quality,
                    'language': 'fr', 'url': but_magnet_link, 'info': info, 'direct': False, 'debridonly': True,
                    'size': dsize,
                    'package': package}

            self._debug_it('APPEND PACKS filename= %s' % filename)
            self._debug_it('APPEND PACKS quality= %s size= %s' % (quality, isize))
            self._debug_it('APPEND PACKS magnet= %s' % but_magnet_link)
            self._debug_it('APPEND PACKS seeders= %s hash= %s filename= %s nameInfo= %s quality= %s size= %s url= %s' % (
                seeders, hash40, filename, name_info, quality, isize, but_magnet_link))
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
        # self.sources(tests.data_movie_2(), '')
        # self.sources(tests.data_movie_3(), '')
        # self.sources(tests.data_movie_4(), '')
        # self.sources(tests.data_serie_1(), '')
        # self.sources(tests.data_serie_2(), '')
        #self.sources(tests.data_serie_3(), '')
        self.sources(tests.data_serie_4(), '')

        #self.sources_packs(tests.data_serie_packs_1(), '')
        #self.sources_packs(tests.data_serie_packs_2(), '')
        #self.sources_packs(tests.data_serie_packs_3(), '')


if __name__ == "__main__":
    ygg = source()
    ygg.main()
