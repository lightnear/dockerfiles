import logging
import os
import sqlite3
import threading
import time

from app.utils import singleton

lock = threading.Lock()

@singleton
class MediaDb:
    logger = None
    db_path = None
    media_db = None

    def __init__(self, config_path):
        self.logger = logging.getLogger(__name__)
        self.db_path = os.path.join(config_path, 'media.db')
        self.media_db = sqlite3.connect(database=self.db_path, timeout=5, check_same_thread=False)
        self.__init_tables()

    def __init_tables(self):
        with lock:
            cursor = self.media_db.cursor()
            try:
                sql = '''
                CREATE TABLE IF NOT EXISTS media
                  (id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
                   title text,
                   year text,
                   media_type text,
                   douban_id integer,
                   tmdb_id integer,
                   imdb_id text,
                   tvdb_id integer,
                   emby_id integer,
                   status text,
                   douban_top250 integer,
                   imdb_top250 integer,
                   create_time text,
                   update_time text
                   );
                '''
                cursor.execute(sql)
                self.media_db.commit()
            except Exception as e:
                self.logger.error(f"【DB】创建数据库错误：{e}")
            finally:
                cursor.close()

    def __excute(self, sql, data=None):
        if not sql:
            return False
        with lock:
            cursor = self.media_db.cursor()
            try:
                if data:
                    cursor.execute(sql, data)
                else:
                    cursor.execute(sql)
                self.media_db.commit()
            except Exception as e:
                print(str(e))
                return False
            finally:
                cursor.close()
            return True

    def __select(self, sql, data):
        if not sql:
            return False
        with lock:
            cursor = self.media_db.cursor()
            try:
                if data:
                    res = cursor.execute(sql, data)
                else:
                    res = cursor.execute(sql)
                ret = res.fetchall()
            except Exception as e:
                print(str(e))
                return []
            finally:
                cursor.close()
            return ret

    def insert(self, server_type, iteminfo):
        if not server_type or not iteminfo:
            return False
        self.delete(server_type, iteminfo.get("id"))
        return self.__excute("INSERT INTO MEDIASYNC_ITEMS "
                             "(SERVER, LIBRARY, ITEM_ID, ITEM_TYPE, TITLE, ORGIN_TITLE, YEAR, TMDBID, IMDBID, PATH, JSON) "
                             "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                             (server_type,
                              iteminfo.get("library"),
                              iteminfo.get("id"),
                              iteminfo.get("type"),
                              iteminfo.get("title"),
                              iteminfo.get("originalTitle"),
                              iteminfo.get("year"),
                              iteminfo.get("tmdbid"),
                              iteminfo.get("imdbid"),
                              iteminfo.get("path"),
                              iteminfo.get("json")
                              ))

    def delete(self, server_type, itemid):
        if not server_type or not itemid:
            return False
        return self.__excute("DELETE FROM MEDIASYNC_ITEMS WHERE SERVER = ? AND ITEM_ID = ?",
                             (server_type, itemid))

    def empty(self, server_type, library):
        if not server_type or not library:
            return False
        return self.__excute("DELETE FROM MEDIASYNC_ITEMS WHERE SERVER = ? AND LIBRARY = ?",
                             (server_type, library))

    def statistics(self, server_type, total_count, movie_count, tv_count):
        if not server_type:
            return False
        self.__excute("DELETE FROM MEDIASYNC_STATISTICS WHERE SERVER = ?", (server_type,))
        return self.__excute("INSERT INTO MEDIASYNC_STATISTICS "
                             "(SERVER, TOTAL_COUNT, MOVIE_COUNT, TV_COUNT, UPDATE_TIME) "
                             "VALUES (?, ?, ?, ?, ?)", (server_type,
                                                        total_count,
                                                        movie_count,
                                                        tv_count,
                                                        time.strftime('%Y-%m-%d %H:%M:%S',
                                                                      time.localtime(time.time()))))

    def exists(self, server_type, title, year, tmdbid):
        if not server_type or not title:
            return False
        if title and year:
            ret = self.__select("SELECT COUNT(1) FROM MEDIASYNC_ITEMS WHERE SERVER = ? AND TITLE = ? AND YEAR = ?",
                                (server_type, title, year))
        else:
            ret = self.__select("SELECT COUNT(1) FROM MEDIASYNC_ITEMS WHERE SERVER = ? AND TITLE = ?",
                                (server_type, title))
        if ret and ret[0][0] > 0:
            return True
        elif tmdbid:
            ret = self.__select("SELECT COUNT(1) FROM MEDIASYNC_ITEMS WHERE TMDBID = ?",
                                (tmdbid,))
            if ret and ret[0][0] > 0:
                return True
        return False

    def get_statistics(self, server_type):
        if not server_type:
            return None
        return self.__select(
            "SELECT TOTAL_COUNT, MOVIE_COUNT, TV_COUNT, UPDATE_TIME FROM MEDIASYNC_STATISTICS WHERE SERVER = ?",
            (server_type,))
