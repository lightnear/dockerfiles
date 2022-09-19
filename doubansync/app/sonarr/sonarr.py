import json
import logging

import requests

from app.utils import RequestUtils

class Sonarr(object):
    logger = None
    base_url = None
    api_key = None
    requests = None
    rootFolderPath = None
    qualityProfileId = None
    monitored = None
    seasonFolder = None

    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        base_url = config.get('sonarr').get('base_url')
        if base_url:
            self.base_url = base_url
        api_key = config.get('sonarr').get('api_key')
        if api_key:
            self.api_key = api_key
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'X-Api-Key': self.api_key,
            "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
        }
        self.requests = RequestUtils(headers=headers, session=requests.Session())
        self.rootFolderPath = "/share/media/tv"
        self.qualityProfileId = 6
        self.monitored = True
        self.seasonFolder = True

    def system_status(self):
        url = f'{self.base_url}/system/status'
        rsp = self.requests.get(url)
        return rsp.json() if rsp else None

    def get_series(self):
        url = f'{self.base_url}/series'
        rsp = self.requests.get(url)
        return rsp.json() if rsp else None

    def lookup_series_by_tvdb(self, tvdb_id):
        url = f'{self.base_url}/series/lookup'
        params = {
            'term': 'tvdb:' + str(tvdb_id)
        }
        rsp = self.requests.get(url, params)
        return rsp.json() if rsp else None

    def add_series(self, media, rootFolderPath=None, qualityProfileId=None, monitored=None, seasonFolder=None):
        tvdb_id = media.tvdb_id
        imdb_id = media.imdb_id
        title = media.title
        year = media.year

        rsp = None
        data = {}

        if not tvdb_id:
            self.logger.warning(f'[sonarr] 没有 tvdb id，无法添加 {title}.{year}')
            return -1
        else:
            rsp = self.lookup_series_by_tvdb(tvdb_id)

        if not rsp:
            self.logger.warning(f'[sonarr] 未搜索到匹配的剧集，无法添加 {title}.{year}')
            return -1

        rsp = rsp[0]
        data['title'] = rsp.get('title')
        data['year'] = rsp.get('year')
        data['titleSlug'] = rsp.get('titleSlug')
        data['tvdbId'] = rsp.get('tvdbId')
        data['imdbId'] = rsp.get('imdbId')
        data['languageProfileId'] = 1
        data['rootFolderPath'] = rootFolderPath if rootFolderPath else self.rootFolderPath
        data['qualityProfileId'] = qualityProfileId if qualityProfileId else self.qualityProfileId
        data['monitored'] = monitored if monitored else self.monitored
        data['seasonFolder'] = seasonFolder if seasonFolder else self.seasonFolder
        data['images'] = json.loads(json.dumps(rsp["images"]))
        data['seasons'] = json.loads(json.dumps(rsp["seasons"]))
        data['addOptions'] = {
            "ignoreEpisodesWithFiles": True,
            "ignoreEpisodesWithoutFiles": False,
            "searchForMissingEpisodes": True
        }
        # self.logger.debug(json.dumps(data))
        url = f'{self.base_url}/series'
        rsp = self.requests.post(url=url, data=json.dumps(data))
        if rsp.status_code == 201:
            self.logger.info(f'[sonarr] 成功添加剧集 {title}.{year}')
            return 1
        elif rsp.status_code == 400:
            self.logger.info(f'[sonarr] 剧集已经存在 {title}.{year}')
            return 1
        else:
            self.logger.error(f'[sonarr] 添加剧集失败 {title}.{year}')
            self.logger.debug(rsp.text)
