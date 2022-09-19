from app.db import DBHelper
from app.media import Media
from app.types import MediaType

# from app.utils import StringUtils


class SqlHelper:

    @staticmethod
    def save_media(media):
        if not media:
            return
        sql = """
        insert into media (title, "year", media_type, douban_id, tmdb_id, imdb_id, tvdb_id, emby_id, status, douban_rank,
                   imdb_rank, create_time, update_time, sync_time)
        values (?, ?, ?,  ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        return DBHelper().insert(sql, (media.title,
                                       media.year,
                                       media.media_type.value,
                                       media.douban_id,
                                       media.tmdb_id,
                                       media.imdb_id,
                                       media.tvdb_id,
                                       media.emby_id,
                                       media.status,
                                       media.douban_rank,
                                       media.imdb_rank,
                                       media.create_time,
                                       media.update_time,
                                       media.sync_time))

    @staticmethod
    def update_media(media):
        if not media:
            return
        sql = """
        update media
        set title = ?, "year" = ?, media_type = ?, douban_id = ?, tmdb_id = ?, imdb_id = ?, tvdb_id = ?, emby_id = ?,
            status = ?, douban_rank = ?, imdb_rank = ?, create_time = ?, update_time = ?, sync_time = ?
        where id = ?
        """
        return DBHelper().update(sql, (media.title,
                                       media.year,
                                       media.media_type.value,
                                       media.douban_id,
                                       media.tmdb_id,
                                       media.imdb_id,
                                       media.tvdb_id,
                                       media.emby_id,
                                       media.status,
                                       media.douban_rank,
                                       media.imdb_rank,
                                       media.create_time,
                                       media.update_time,
                                       media.sync_time,
                                       media.id))

    @staticmethod
    def update_douban_ranks(douban_ids: list):
        """
        插入或更新豆瓣 TOP250信息
        """
        if not douban_ids:
            return
        sql = """
        update media set douban_rank = null where douban_id not in (%s)
        """
        sql = sql % ','.join('?'*len(douban_ids))
        return DBHelper().update(sql, douban_ids)

    @staticmethod
    def update_imdb_ranks(imdb_ids: list):
        """
        插入或更新IMDB TOP250信息
        """
        if not imdb_ids:
            return
        sql = """
        update media set imdb_rank = null where imdb_id not in (%s)
        """
        sql = sql % ','.join('?'*len(imdb_ids))
        return DBHelper().update(sql, imdb_ids)

    @staticmethod
    def search_medias():
        """
        从数据库中查询全部记录
        """
        sql = """
        select * from media
        """
        rows = DBHelper().select(sql)
        if not rows:
            return None
        medias = []
        for row in rows:
            media = Media()
            media.id = row[0]
            media.title = row[1]
            media.year = row[2]
            media.media_type = MediaType.MOVIE if row[3] == MediaType.MOVIE.value else MediaType.TV
            media.douban_id = row[4]
            media.tmdb_id = row[5]
            media.imdb_id = row[6]
            media.tvdb_id = row[7]
            media.emby_id = row[8]
            media.status = row[9]
            media.douban_rank = row[10]
            media.imdb_rank = row[11]
            media.create_time = row[12]
            media.update_time = row[13]
            media.sync_time = row[14]
            medias.append(media)
        return medias

    @staticmethod
    def search_medias_by_status(status):
        """
        从数据库中查询全部记录
        """
        sql = """
        select * from media where status = ?
        """
        rows = DBHelper().select(sql, (status,))
        if not rows:
            return None
        medias = []
        for row in rows:
            media = Media()
            media.id = row[0]
            media.title = row[1]
            media.year = row[2]
            media.media_type = MediaType.MOVIE if row[3] == MediaType.MOVIE.value else MediaType.TV
            media.douban_id = row[4]
            media.tmdb_id = row[5]
            media.imdb_id = row[6]
            media.tvdb_id = row[7]
            media.emby_id = row[8]
            media.status = row[9]
            media.douban_rank = row[10]
            media.imdb_rank = row[11]
            media.create_time = row[12]
            media.update_time = row[13]
            media.sync_time = row[14]
            medias.append(media)
        return medias

    @staticmethod
    def select_douban_top250():
        """
        查询豆瓣 TOP250
        :return:
        """
        sql = """
        select * from media where douban_rank is not null order by douban_rank
        """
        rows = DBHelper().select(sql)
        if not rows:
            return None
        medias = []
        for row in rows:
            media = Media()
            media.id = row[0]
            media.title = row[1]
            media.year = row[2]
            media.media_type = MediaType.MOVIE if row[3] == MediaType.MOVIE.value else MediaType.TV
            media.douban_id = row[4]
            media.tmdb_id = row[5]
            media.imdb_id = row[6]
            media.tvdb_id = row[7]
            media.emby_id = row[8]
            media.status = row[9]
            media.douban_rank = row[10]
            media.imdb_rank = row[11]
            media.create_time = row[12]
            media.update_time = row[13]
            media.sync_time = row[14]
            medias.append(media)
        return medias


    @staticmethod
    def select_imdb_top250():
        """
        查询IMDB TOP250
        :return:
        """
        sql = """
        select * from media where imdb_rank is not null order by imdb_rank
        """
        rows = DBHelper().select(sql)
        if not rows:
            return None
        medias = []
        for row in rows:
            media = Media()
            media.id = row[0]
            media.title = row[1]
            media.year = row[2]
            media.media_type = MediaType.MOVIE if row[3] == MediaType.MOVIE.value else MediaType.TV
            media.douban_id = row[4]
            media.tmdb_id = row[5]
            media.imdb_id = row[6]
            media.tvdb_id = row[7]
            media.emby_id = row[8]
            media.status = row[9]
            media.douban_rank = row[10]
            media.imdb_rank = row[11]
            media.create_time = row[12]
            media.update_time = row[13]
            media.sync_time = row[14]
            medias.append(media)
        return medias

    @staticmethod
    def select_media_by_douban(douban_id):
        sql = """
        select * from media where douban_id = ?
        """
        rows = DBHelper().select(sql, (douban_id,))
        if not rows:
            return None
        row = rows[0]
        media = Media()
        media.id = row[0]
        media.title = row[1]
        media.year = row[2]
        media.media_type = MediaType.MOVIE if row[3] == MediaType.MOVIE.value else MediaType.TV
        media.douban_id = row[4]
        media.tmdb_id = row[5]
        media.imdb_id = row[6]
        media.tvdb_id = row[7]
        media.emby_id = row[8]
        media.status = row[9]
        media.douban_rank = row[10]
        media.imdb_rank = row[11]
        media.create_time = row[12]
        media.update_time = row[13]
        media.sync_time = row[14]
        return media


    @staticmethod
    def select_media_by_tmdb(tmdb_id):
        sql = """
        select * from media where tmdb_id = ?
        """
        rows = DBHelper().select(sql, (tmdb_id,))
        if not rows:
            return None
        row = rows[0]
        media = Media()
        media.id = row[0]
        media.title = row[1]
        media.year = row[2]
        media.media_type = MediaType.MOVIE if row[3] == MediaType.MOVIE.value else MediaType.TV
        media.douban_id = row[4]
        media.tmdb_id = row[5]
        media.imdb_id = row[6]
        media.tvdb_id = row[7]
        media.emby_id = row[8]
        media.status = row[9]
        media.douban_rank = row[10]
        media.imdb_rank = row[11]
        media.create_time = row[12]
        media.update_time = row[13]
        media.sync_time = row[14]
        return media

    @staticmethod
    def select_media_by_imdb(imdb_id):
        sql = """
        select * from media where imdb_id = ?
        """
        rows =  DBHelper().select(sql, (imdb_id,))
        if not rows:
            return None
        media = Media()
        row = rows[0]
        media.id = row[0]
        media.title = row[1]
        media.year = row[2]
        media.media_type = MediaType.MOVIE if row[3] == MediaType.MOVIE.value else MediaType.TV
        media.douban_id = row[4]
        media.tmdb_id = row[5]
        media.imdb_id = row[6]
        media.tvdb_id = row[7]
        media.emby_id = row[8]
        media.status = row[9]
        media.douban_rank = row[10]
        media.imdb_rank = row[11]
        media.create_time = row[12]
        media.update_time = row[13]
        media.sync_time = row[14]
        return media

    @staticmethod
    def select_media_by_tvdb(tvdb_id):
        sql = """
        select * from media where tvdb_id = ?
        """
        rows = DBHelper().select(sql, (tvdb_id,))
        if not rows:
            return None
        media = Media()
        row = rows[0]
        media.id = row[0]
        media.title = row[1]
        media.year = row[2]
        media.media_type = MediaType.MOVIE if row[3] == MediaType.MOVIE.value else MediaType.TV
        media.douban_id = row[4]
        media.tmdb_id = row[5]
        media.imdb_id = row[6]
        media.tvdb_id = row[7]
        media.emby_id = row[8]
        media.status = row[9]
        media.douban_rank = row[10]
        media.imdb_rank = row[11]
        media.create_time = row[12]
        media.update_time = row[13]
        media.sync_time = row[14]
        return media
