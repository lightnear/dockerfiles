import logging
from time import sleep

import requests

from app.utils import RequestUtils


class Imdb(object):
    logger = None
    base_url = None
    api_key = None
    requests = None

    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        base_url = config.get('imdb').get('base_url')
        if base_url:
            self.base_url = base_url
        api_key = config.get('imdb').get('api_key')
        if api_key:
            self.api_key = api_key
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
        }
        self.requests = RequestUtils(headers=headers, session=requests.Session())

    def imdb_top250(self):
        imdb_ids = []
        url = f'{self.base_url}/Top250Movies/{self.api_key}'
        rsp = self.requests.get(url)
        sleep(1)
        # self.logger.debug(rsp)
        if not rsp:
            self.logger.warning('[imdb] 获取IMDB TOP250信息失败')
        for imdb in rsp.json().get('items'):
            imdb_id = imdb.get('id')
            imdb_ids.append(imdb_id)
        return imdb_ids
