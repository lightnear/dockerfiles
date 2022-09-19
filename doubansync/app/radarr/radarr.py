import json
import logging

import requests

from app.media import Media
from app.utils import MediaType
from app.utils import RequestUtils


class Radarr(object):
    logger = None
    base_url = None
    api_key = None
    requests = None
    rootFolderPath = None
    qualityProfileId = None
    monitored = None
    minimumAvailability = None

    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        base_url = config.get('radarr').get('base_url')
        if base_url:
            self.base_url = base_url
        api_key = config.get('radarr').get('api_key')
        if api_key:
            self.api_key = api_key
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'X-Api-Key': self.api_key,
            "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
        }
        self.requests = RequestUtils(headers=headers, session=requests.Session())
        self.rootFolderPath = "/share/media/movie"
        self.qualityProfileId = 6
        self.monitored = True
        self.minimumAvailability = 'Released'

    def system_status(self):
        url = f'{self.base_url}/system/status'
        rsp = self.requests.get(url)
        return rsp.json() if rsp else None

    def get_movies(self):
        url = f'{self.base_url}/movie'
        rsp = self.requests.get(url)
        return rsp.json() if rsp else None

    def get_movie_by_tmdb(self, tmdb_id):
        url = f'{self.base_url}/movie'
        params = {
            'tmdbId': tmdb_id
        }
        rsp = self.requests.get(url, params)
        return rsp.json() if rsp else None

    def lookup_movie_by_tmdb(self, tmdb_id):
        url = f'{self.base_url}/movie/lookup/tmdb'
        params = {
            'tmdbId': tmdb_id
        }
        rsp = self.requests.get(url, params)
        return rsp.json() if rsp else None

    def lookup_movie_by_imdb(self, imdb_id):
        url = f'{self.base_url}/movie/lookup/imdb'
        params = {
            'imdbId': imdb_id
        }
        rsp = self.requests.get(url, params)
        return rsp.json() if rsp else None

    def add_movie(self, media, rootFolderPath=None, qualityProfileId=None, monitored=None, minimumAvailability=None):
        tmdb_id = media.tmdb_id
        imdb_id = media.imdb_id
        title = media.title
        year = media.year

        if not tmdb_id and not imdb_id:
            self.logger.warning(f'[radarr] 没有 tmdb id 和 imdb id，无法添加 {title}.{year}')
            return None

        rsp = None
        data = {}
        if tmdb_id:
            rsp = self.lookup_movie_by_tmdb(tmdb_id)
        elif imdb_id:
            rsp = self.lookup_movie_by_imdb(imdb_id)

        if not rsp:
            self.logger.warning(f'[radarr] 未搜索到匹配的电影，无法添加 {title}.{year}')
            return None

        data['title'] = rsp.get('title')
        data['year'] = rsp.get('year')
        data['titleSlug'] = rsp.get('titleSlug')
        data['tmdbId'] = rsp.get('tmdbId')
        data['imdbId'] = rsp.get('imdbId')
        data['rootFolderPath'] = rootFolderPath if rootFolderPath else self.rootFolderPath
        data['qualityProfileId'] = qualityProfileId if qualityProfileId else self.qualityProfileId
        data['monitored'] = monitored if monitored else self.monitored
        data['minimumAvailability'] = minimumAvailability if minimumAvailability else self.minimumAvailability
        data['images'] = json.loads(json.dumps(rsp.get('images')))
        data['addOptions'] = {
            "searchForMovie": True
        }
        url = f'{self.base_url}/movie'
        rsp = self.requests.post(url=url, data=json.dumps(data))
        if rsp.status_code == 201:
            self.logger.info(f'[radarr] 成功添加电影 {title}.{year}')
            return 1
        else:
            self.logger.error(f'[radarr] 添加电影失败 {title}.{year}')
            self.logger.debug(rsp.status_code)
            self.logger.debug(rsp.text)
            return None

    def imdb2media(self, imdb_id):
        rsp = self.lookup_movie_by_imdb(imdb_id)
        if not rsp:
            return None
        media = Media()
        media.title = rsp.get('title')
        media.year = rsp.get('year')
        media.media_type = MediaType.MOVIE
        # media.douban_id = None
        media.tmdb_id = rsp.get('tmdbId')
        media.imdb_id = rsp.get('imdbId')
        # media.tvdb_id = None
        # media.emby_id = None
        status = self.get_movie_by_tmdb(media.tmdb_id)
        media.status = 'add' if status else 'wait'
        # media.douban_rank = None
        # media.imdb_rank = None
        return media
