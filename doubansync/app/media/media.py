import datetime


class MetaInfo(object):

    title: str = None
    year: int = None
    media_type: str = None
    douban_id: int = None
    tmdb_id: int = None
    imdb_id: str = None
    tvdb_id: int = None
    emby_id: int = None
    status: str = None
    create_time: datetime = datetime.datetime.now()
    update_time: datetime = datetime.datetime.now()

    def __init__(self):
        pass

    # def __init__(self, title, year):
    #     self.title = title
    #     self.year = year

    def __str__(self):
        info = {
            'title': self.title,
            'year': self.year,
            'media_type': self.media_type,
            'douban_id': self.douban_id,
            'tmdb_id': self.tmdb_id,
            'imdb_id': self.imdb_id,
            'tvdb_id': self.tvdb_id,
            'emby_id': self.emby_id,
            'status': self.status,
            'create_time': self.create_time,
            'update_time': self.update_time
        }
        return str(info)

    def set_title(self, title):
        self.title = title

    def get_title(self):
        return self.title

    def set_year(self, year):
        self.year = year

    def get_year(self):
        return self.year

    def set_media_type(self, media_type):
        self.media_type = media_type

    def get_media_type(self):
        return self.media_type

    def set_douban_id(self, douban_id):
        self.douban_id = douban_id

    def get_douban_id(self):
        return self.douban_id

    def set_tmdb_id(self, tmdb_id):
        self.tmdb_id = tmdb_id

    def get_tmdb_id(self):
        return self.tmdb_id

    def set_imdb_id(self, imdb_id):
        self.imdb_id = imdb_id

    def get_imdb_id(self):
        return self.imdb_id

    def set_tvdb_id(self, tvdb_id):
        self.tvdb_id = tvdb_id

    def get_tvdb_id(self):
        return self.tvdb_id

    def set_emby_id(self, emby_id):
        self.emby_id = emby_id

    def get_emby_id(self):
        return self.emby_id

    def set_status(self, status):
        self.status = status

    def get_status(self):
        return self.status

