import logging
from urllib.parse import urlencode

import requests

from app.utils import RequestUtils


class Emby(object):
    logger = None
    host = None
    api_key = None
    requests = None

    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        host = config.get('emby').get('host')
        if host:
            self.host = host
        api_key = config.get('emby').get('api_key')
        if api_key:
            self.api_key = api_key
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'X-Emby-Token': self.api_key,
            "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
        }
        self.requests = RequestUtils(headers=headers, session=requests.Session())

    def system_info(self):
        url = f'{self.host}/emby/System/Info'
        rsp = self.requests.get(url)
        return rsp.json() if rsp else None

    def items_count(self):
        url = f'{self.host}/emby/Items/Counts'
        rsp = self.requests.get(url)
        return rsp.json() if rsp else None

    def search_movie_by_tmdb(self, tmdb_id):
        url = f'{self.host}/emby/Items'
        params = {
            'IncludeItemTypes': 'Movie',
            'Fields': 'ProductionYear,ProviderIds,MediaType',
            'Recursive': True,
            'StartIndex': 0,
            'Limit': 10,
            'AnyProviderIdEquals': f'tmdb.{tmdb_id}'
        }
        rsp = self.requests.get(url, params)
        return rsp.json() if rsp else None

    def search_movie_by_imdb(self, imdb_id):
        url = f'{self.host}/emby/Items'
        params = {
            'IncludeItemTypes': 'Movie',
            'Fields': 'ProductionYear,ProviderIds,MediaType',
            'Recursive': True,
            'StartIndex': 0,
            'Limit': 10,
            'AnyProviderIdEquals': f'imdb.{imdb_id}'
        }
        rsp = self.requests.get(url, params)
        return rsp.json() if rsp else None

    def search_series_by_tvdb(self, tvdb_id):
        url = f'{self.host}/emby/Items'
        params = {
            'IncludeItemTypes': 'Series',
            'Fields': 'ProductionYear,ProviderIds,MediaType',
            'Recursive': True,
            'StartIndex': 0,
            'Limit': 10,
            'AnyProviderIdEquals': f'tvdb.{tvdb_id}'
        }
        rsp = self.requests.get(url, params)
        return rsp.json() if rsp else None

    def search_series_by_tmdb(self, tmdb_id):
        url = f'{self.host}/emby/Items'
        params = {
            'IncludeItemTypes': 'Series',
            'Fields': 'ProductionYear,ProviderIds,MediaType',
            'Recursive': True,
            'StartIndex': 0,
            'Limit': 10,
            'AnyProviderIdEquals': f'tmdb.{tmdb_id}'
        }
        rsp = self.requests.get(url, params)
        return rsp.json() if rsp else None

    def search_series_by_imdb(self, imdb_id):
        url = f'{self.host}/emby/Items'
        params = {
            'IncludeItemTypes': 'Series',
            'Fields': 'ProductionYear,ProviderIds,MediaType',
            'Recursive': True,
            'StartIndex': 0,
            'Limit': 10,
            'AnyProviderIdEquals': f'imdb.{imdb_id}'
        }
        rsp = self.requests.get(url, params)
        return rsp.json() if rsp else None

    def create_playlist(self, name, emby_ids):
        str_emby_ids = ','.join(str(emby_id) for emby_id in emby_ids)
        url = f'{self.host}/emby/Playlists'
        params = {
            'Name': name,
            'Ids': str_emby_ids
        }
        rsp = self.requests.post(url=url, params=urlencode(params))
        return rsp.json() if rsp else None

    def search_playlist(self, name):
        url = f'{self.host}/emby/Items'
        params = {
            'IncludeItemTypes': 'Playlist',
            'Fields': 'ProductionYear,ProviderIds,MediaType',
            'Recursive': True,
            'StartIndex': 0,
            'Limit': 100,
            'SearchTerm': name
        }
        rsp = self.requests.get(url, params)
        return rsp.json() if rsp else None

    def get_playlist_items(self, playlist_id):
        url = f'{self.host}/emby/Playlists/{playlist_id}/Items'
        params = {
            'StartIndex': 0,
            'Limit': 10000,
            'Fields': 'ProductionYear,ProviderIds,MediaType'
        }
        rsp = self.requests.get(url, params)
        return rsp.json() if rsp else None

    def add_playlist_items(self, playlist_id, emby_ids):
        str_emby_ids = ','.join(str(emby_id) for emby_id in emby_ids)
        url = f'{self.host}/emby/Playlists/{playlist_id}/Items?Ids={str_emby_ids}'
        rsp = self.requests.post(url)
        if rsp.status_code >= 200 and rsp.status_code < 300:
            return True
        else:
            return None

    def remove_playlist_items(self, playlist_id, entry_ids):
        url = f'{self.host}/emby/Playlists/{playlist_id}/Items'
        entry_ids = ','.join(str(entry_id) for entry_id in entry_ids)
        params = {
            'EntryIds': entry_ids
        }
        rsp = self.requests.request('DELETE', url, params=params)
        if rsp.status_code >= 200 and rsp.status_code < 300:
            return True
        else:
            return None

    def move_playlist_item(self, playlist_id, item_id, new_index):
        url = f'{self.host}/emby/Playlists/{playlist_id}/Items/{item_id}/Move/{new_index}'
        rsp = self.requests.post(url)
        if rsp.status_code >= 200 and rsp.status_code < 300:
            return True
        else:
            return None
