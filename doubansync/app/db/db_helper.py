import os
import threading

import logging
from app.utils import singleton
from app.db import DBPool

lock = threading.Lock()


@singleton
class DBHelper:
    logger = None
    __connection = None
    __db_path = None
    __pools = None

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.init_config()
        self.__init_tables()
        self.__cleardata()
        self.__initdata()

    def init_config(self):
        config_path = os.environ.get('DB_CONFIG_PATH')
        self.logger.info(f'config path: {config_path}')
        self.__db_path = os.path.join(config_path, 'media.db')
        self.__pools = DBPool(
            max_active=5, max_wait=20, init_size=5, db_type="SQLite3",
            **{'database': self.__db_path, 'check_same_thread': False, 'timeout': 15})

    def __init_tables(self):
        conn = self.__pools.get()
        cursor = conn.cursor()
        try:
            # 媒体信息表
            sql = '''
            create table media
            (
                id            INTEGER not null
                    primary key autoincrement,
                title         TEXT,
                year          TEXT,
                media_type    TEXT,
                douban_id     INTEGER,
                tmdb_id       INTEGER,
                imdb_id       TEXT,
                tvdb_id       INTEGER,
                emby_id       INTEGER,
                status        TEXT,
                douban_rank INTEGER,
                imdb_rank   INTEGER,
                create_time   TEXT,
                update_time   TEXT,
                sync_time     TEXT
            );
            '''
            cursor.execute(sql)
            # 提交
            conn.commit()

        except Exception as e:
            self.logger.error(f"[DB]创建数据库错误：{e}")
        finally:
            cursor.close()
            self.__pools.free(conn)

    def __cleardata(self):
        pass

    def __initdata(self):
        pass

    def __excute(self, sql, data=None):
        if not sql:
            return False
        with lock:
            conn = self.__pools.get()
            cursor = conn.cursor()
            try:
                if data:
                    cursor.execute(sql, data)
                else:
                    cursor.execute(sql)
                conn.commit()
            except Exception as e:
                self.logger.error(f"[DB] 执行SQL出错：sql:{sql}; parameters:{data}; {e}")
                return False
            finally:
                cursor.close()
                self.__pools.free(conn)
            return True

    def __excute_many(self, sql, data_list):
        if not sql or not data_list:
            return False
        with lock:
            conn = self.__pools.get()
            cursor = conn.cursor()
            try:
                cursor.executemany(sql, data_list)
                conn.commit()
            except Exception as e:
                self.logger.error(f"[DB] 执行SQL出错：sql:{sql}; {e}")
                return False
            finally:
                cursor.close()
                self.__pools.free(conn)
            return True

    def __select(self, sql, data):
        if not sql:
            return False
        with lock:
            conn = self.__pools.get()
            cursor = conn.cursor()
            try:
                if data:
                    res = cursor.execute(sql, data)
                else:
                    res = cursor.execute(sql)
                ret = res.fetchall()
            except Exception as e:
                self.logger.error(f"[DB] 执行SQL出错：sql:{sql}; parameters:{data}; {e}")
                return []
            finally:
                cursor.close()
                self.__pools.free(conn)
            return ret

    def insert(self, sql, data=None):
        """
        执行新增
        :param sql: SQL语句
        :param data: 数据，需为列表或者元祖
        :return: 执行状态
        """
        return self.__excute(sql, data)

    def delete(self, sql, data=None):
        """
        执行删除
        :param sql: SQL语句
        :param data: 数据，需为列表或者元祖
        :return: 执行状态
        """
        return self.__excute(sql, data)

    def update(self, sql, data=None):
        """
        执行更新或删除
        :param sql: SQL语句
        :param data: 数据，需为列表或者元祖
        :return: 执行状态
        """
        return self.__excute(sql, data)

    def update_batch(self, sql, data_list):
        """
        执行更新或删除
        :param sql: 批量更新SQL语句
        :param data_list: 数据列表
        :return: 执行状态
        """
        return self.__excute_many(sql, data_list)

    def select(self, sql, data=None):
        """
        执行查询
        :param sql: 查询的SQL语句
        :param data: 数据，需为列表或者元祖
        :return: 查询结果的二级列表
        """
        return self.__select(sql, data)
