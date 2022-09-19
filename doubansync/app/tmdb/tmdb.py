import logging
import re

import requests
from cn2an import cn2an

from app.types import MediaType
from app.utils import RequestUtils

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode


class Tmdb(object):
    logger = None
    base_url = None
    token = None
    proxies = None
    requests = None

    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        base_url = config.get('tmdb').get('base_url')
        if base_url:
            self.base_url = base_url
        token = config.get('tmdb').get('token')
        if token:
            self.token = token
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Authorization': f'Bearer {token}',
            "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
        }
        proxies = config.get('tmdb').get('proxies')
        if proxies:
            self.proxies = proxies
        if self.proxies:
            self.requests = RequestUtils(headers=headers, session=requests.Session(), proxies=proxies)
        else:
            self.requests = RequestUtils(headers=headers, session=requests.Session())

    def __invoke(self, url, params=None):
        rsp = self.requests.get(url=url, params=params)
        return rsp.json() if rsp else None

    def movie_detail(self, tmdb_id):
        url = f'{self.base_url}/movie/{tmdb_id}'
        params = {
            'language': 'zh-CN',
            # 'append_to_response': 'videos,trailers,images,credits,alternative_titles,translations,external_ids'
            'append_to_response': 'external_ids'
        }
        return self.__invoke(url, params)

    def series_detail(self, tmdb_id):
        url = f'{self.base_url}/tv/{tmdb_id}'
        params = {
            'language': 'zh-CN',
            # 'append_to_response': 'videos,trailers,images,credits,alternative_titles,translations,external_ids'
            'append_to_response': 'external_ids'
        }
        return self.__invoke(url, params)

    def series_seasons(self, tmdb_id):
        if not  tmdb_id:
            return []
        series_info = self.series_detail(tmdb_id)
        if not series_info:
            return []
        season_info = series_info.get('seasons')
        if not season_info:
            return []
        seasons = []
        for season in season_info:
            if season.get("season_number") != 0 and season.get("episode_count") != 0:
                seasons.append({
                    'id': season.get('id'),
                    'season_number': season.get('season_number'),
                    'episode_count': season.get('episode_count'),
                    'air_date': season.get('air_date'),
                    'air_year': int(season.get('air_date')[0:4])
                })
        return seasons

    def search_movies(self, title, year=None):
        url = f'{self.base_url}/search/movie'
        params = {
            'query': title,
            'language': 'zh-CN',
            'include_adult': True
        }
        if year:
            params.update(year=year)
        return self.__invoke(url, urlencode(params))

    def search_series(self, title, year=None):
        url = f'{self.base_url}/search/tv'
        params = {
            'query': title,
            'language': 'zh-CN',
            'include_adult': True
        }
        if year:
            params.update(year=year)
        return self.__invoke(url, urlencode(params))

    def match_movie(self, title, year):
        """
        根据名称和年份匹配电影
        :param title:
        :param year:
        :return:
        """
        try:
            rsp = self.search_movies(title, year)
        except Exception as e:
            self.logger.error(f"[tmdb] 连接TMDB出错：{str(e)}")
            return None
        movies = rsp.get('results')
        if len(movies) == 0:
            self.logger.debug(f"[tmdb] {title}.{year} 未找到相关电影信息! 通过名称搜索")
            rsp = self.search_movies(title)
            if len(rsp.get('results')) == 0:
                self.logger.debug(f"[tmdb] {title}.{year} 未找到相关电影信息!")
                return None
            movies = rsp.get('results')
            for movie in movies:
                if movie.get('title') and movie.get('title') == title:
                    return movie.get('id')
        elif len(movies) > 1:
            for movie in movies:
                if movie.get('title') == title:
                    return movie.get('id')
        else:
            return movies[0]['id']

        self.logger.debug(f"[tmdb] {title}.{year} 未找到相关电影信息!")
        return None

    @staticmethod
    def season_title(title: str):
        """
        处理 title 含有 第XX季的情况
        :param title:
        :return:
        """
        pattern = r'[第\s]+([0-9一二三四五六七八九十S\-]+)\s*季'
        rst = re.search(r'%s' % pattern, title, re.I)
        if rst:
            season = cn2an(inputs=rst.group(1), mode='smart')
            title = title.rstrip(rst.group(0))
            return title, season
        pattern = r'(.*?)(\d+)'
        rst = re.search(r'%s' % pattern, title, re.I)
        if rst:
            season = rst.group(2)
            title = title.rstrip(rst.group(2))
            return title, season
        return title, None

    def match_series_by_season(self, title, season_number, year):
        try:
            rsp = self.search_series(title)
        except Exception as e:
            self.logger.error(f"[tmdb] 连接TMDB出错：{str(e)}")
            return None
        series = rsp.get('results')
        if not series:
            self.logger.debug(f"[tmdb] {title}.第{season_number}季.{year} 未找到相关剧集信息!")
            return None
        for tv in series:
            # self.logger.debug(tv)
            if tv.get('name') == title:
                tmdb_id = tv.get('id')
                seasons = self.series_seasons(tmdb_id)
                if not seasons:
                    self.logger.debug(f"[tmdb] {title}.第{season_number}季.{year} 未找到相关剧集信息!")
                    return None
                for season in seasons:
                    if int(season.get('season_number')) == int(season_number) \
                       and int(season.get('air_year')) == int(year):
                        return tmdb_id

        self.logger.debug(f"[tmdb] {title}.第{season_number}季.{year} 未找到相关剧集信息!")
        return None

    def match_series(self, title, year):
        """
        根据名称和年份匹配剧集
        :param title:
        :param year:
        :return:
        """
        rsp = None
        info = {}

        title, season = self.season_title(title)
        # 有季信息时，使用季匹配
        if season:
            self.logger.debug(f'[tmdb] 使用季匹配 {title} {season} {year}')
            return self.match_series_by_season(title, season, year)

        # 没有季信息时，直接搜索剧集名
        try:
            rsp = self.search_series(title, year)
        except Exception as e:
            self.logger.error(f"[tmdb] 连接TMDB出错：{str(e)}")
            return None
        series = rsp.get('results')
        if len(series) == 0:
            self.logger.debug(f"[tmdb] {title}.{year} 未找到相关剧集信息! 通过名称搜索")
            rsp = self.search_series(title)
            if len(rsp.get('results')) == 0:
                self.logger.debug(f"[tmdb] {title}.{year} 未找到相关剧集信息!")
                return None
            series = rsp.get('results')
            for tv in series:
                if tv.get('name') and tv.get('name') == title:
                    return tv.get('id')
        elif len(series) > 1:
            for tv in series:
                if tv.get('name') == title:
                    return tv.get('id')
        else:
            return series[0]['id']
        self.logger.debug(f"[tmdb] {title}.{year} 未找到相关剧集信息!")
        return None

    def match_tmdb(self, media):
        """
        检索tmdb中的媒体信息，匹配返回一条尽可能正确的信息
        :param media:
        :return:
        """
        self.logger.info(f'[tmdb] 正在识别 {media.media_type.value} {media.title} {media.year}')

        if media.media_type == MediaType.MOVIE:
            tmdb_id = self.match_movie(media.title, media.year)
            rsp = self.movie_detail(tmdb_id)
            if not rsp:
                return media
            media.title = rsp.get('title')
            media.year = int(rsp.get('release_date')[0:4])
        else:
            tmdb_id = self.match_series(media.title, media.year)
            rsp = self.series_detail(tmdb_id)
            if not rsp:
                return media
            media.title = rsp.get('name')
            media.year = int(rsp.get('first_air_date')[0:4])

        media.tmdb_id = rsp.get('id')
        media.imdb_id = rsp.get('external_ids').get('imdb_id')
        media.tvdb_id = rsp.get('external_ids').get('tvdb_id')
        self.logger.info(
            f'[tmdb] 识别到媒体信息 {media.media_type.value} {media.title} {media.year}： tmdb.{media.tmdb_id} imdb.{media.imdb_id} tvdb.{media.tvdb_id}')
        return media
