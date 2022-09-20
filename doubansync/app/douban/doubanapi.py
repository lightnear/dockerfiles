import base64
import hashlib
import hmac
import time
from urllib import parse

import requests
import requests_cache
import logging
from app.utils import RequestUtils


class DoubanApi(object):
    logger = None
    user_agent = None
    headers = None
    api_key = None
    base_url = None
    urls = None
    requests = None
    max_retries = None

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.20(0x18001434) NetType/WIFI Language/en'
        self.headers = {
            'User-Agent': self.user_agent,
            'Referer': 'https://servicewechat.com/wx2f9b06c1de1ccfca/84/page-frame.html',
            'Accept-Encoding': 'gzip,compress,deflate',
            'content-type': 'application/json'
        }
        # self.api_secret = 'bf7dddc7c9cfe6f7'
        self.api_key = '0ac44ae016490db2204ce0a042db2916'
        self.base_url = 'https://frodo.douban.com/api/v2'
        self.urls = {
            # 各类主题合集
            # start=0&count=20
            'movie_top250': '/subject_collection/movie_top250/items',
            # 高分经典科幻片榜
            'movie_scifi': '/subject_collection/movie_scifi/items',
            # 高分经典喜剧片榜
            'movie_comedy': '/subject_collection/movie_comedy/items',
            # 高分经典动作片榜
            'movie_action': '/subject_collection/movie_action/items',
            # 高分经典爱情片榜
            'movie_love': '/subject_collection/movie_love/items',
            'tv_chinese_best_weekly': '/subject_collection/tv_chinese_best_weekly/items',
            'tv_global_best_weekly': '/subject_collection/tv_global_best_weekly/items',
            # movie info
            'movie_detail': '/movie/',
            # tv info
            'tv_detail': '/tv/',
        }
        requests_cache.install_cache(backend='memory')
        requests_cache.clear()
        self.requests = RequestUtils(headers=self.headers, session=requests.Session())

    # def get_sig(self, url: str, ts: int, method='GET') -> str:
    #     """
    #     :param url: api
    #     :param ts: 时间戳
    #     :param method: 请求方法（大写 GET POST）
    #     :return:
    #     """
    #     url_path = parse.urlparse(url).path
    #     raw_sign = '&'.join([method.upper(), parse.quote(url_path, safe=''), str(ts)])
    #     return base64.b64encode(
    #         hmac.new("bf7dddc7c9cfe6f7".encode(), raw_sign.encode(), hashlib.sha1).digest()).decode()

    def __invoke(self, url, **kwargs):
        # t_ = int(time.time())
        url = self.base_url + url
        params = {
            'apiKey': self.api_key
        }
        # params = {
        #     "tags": "",
        #     "refresh": 0,
        #     "selected_categories": {},
        #     "start": 0,
        #     "count": 8,
        #     "udid": "c72cfb38a040b64521255795860f17a634090668",
        #     "rom": "android",
        #     "apikey": self.api_key,
        #     "s": "rexxar_new",
        #     "channel": "Baidu_Market",
        #     "timezone": "Asia/Shanghai",
        #     "device_id": "c72cfb38a040b64521255795860f17a634090668",
        #     "os_rom": "android",
        #     "apple": "9efa6ba99021c3c98ef09c7dd7543653",
        #     # "icecream": "84ced86782ed487aca374defabfd29c5",
        #     # "mooncake": "17145441849e2d8e8e757360917238ea",
        #     "sugar": 46000,
        #     "loc_id": 108288,
        #     "_sig": self.get_sig(url=url, ts=t_),
        #     "_ts": t_,
        # }
        if kwargs:
            params.update(kwargs)
        # self.logger.debug(url)
        # self.logger.debug(params)
        rsp = self.requests.get(url=url, params=params)
        # self.logger.debug(rsp.status_code)
        # self.logger.debug(rsp.headers)

        return rsp.json() if rsp else None

    def movie_detail(self, subject_id):
        # self.logger.debug(subject_id)
        return self.__invoke(self.urls["movie_detail"] + str(subject_id))

    def tv_detail(self, subject_id):
        # self.logger.debug(subject_id)
        return self.__invoke(self.urls["tv_detail"] + str(subject_id))

    def movie_top250(self):
        return self.__invoke(self.urls["movie_top250"], start=0, count=250)
