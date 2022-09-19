import datetime


class Media(object):
    id: int = None
    title: str = None
    year: int = None
    media_type: str = None
    douban_id: int = None
    tmdb_id: int = None
    imdb_id: str = None
    tvdb_id: int = None
    emby_id: int = None
    status: str = None
    douban_rank: int = None
    imdb_rank: int = None
    create_time = None
    update_time = None
    sync_time = None

    def __init__(self):
        self.create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.sync_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        media = {'title': self.title, 'year': self.year, 'media_type': self.media_type, 'douban_id': self.douban_id,
            'tmdb_id': self.tmdb_id, 'imdb_id': self.imdb_id, 'tvdb_id': self.tvdb_id, 'emby_id': self.emby_id,
            'status': self.status, 'douban_rank': self.douban_rank, 'imdb_rank': self.imdb_rank,
            'create_time': self.create_time, 'update_time': self.update_time, 'sync_time': self.sync_time}
        return str(media)
