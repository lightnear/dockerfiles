import os
import sys

sys.path.append(os.path.abspath('..'))
import time
import schedule
import argparse
import logging.config
import yaml
from app.media import Media
from app.tmdb import Tmdb
from app.utils import MediaType
from app.emby import Emby
from app.imdb import Imdb
from app.db import SqlHelper

log_config = {}
with open("logging.yml", 'r') as r:
    log_config = yaml.safe_load(r)
logging.config.dictConfig(log_config)
logger = logging.getLogger(__name__)


# 加载配置文件
def load_config(config_path):
    try:
        with open(config_path, 'r', encoding='utf-8') as r:
            config = yaml.safe_load(r)
        return config
    except Exception as e:
        logger.error('加载配置文件失败，请检查配置文件')
        logger.error(e)
        return []


def run_job(name):
    logger.info(name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='douban sync')
    parser.add_argument('-c', '--config', default="../config/config.yml", help='config file')
    args = parser.parse_args()
    config_file = args.config
    config = load_config(config_file)
    config_path, _ = os.path.split(config_file)
    os.environ['DB_CONFIG_PATH'] = os.path.abspath(config_path)
    # logger.debug(config)

    # doubanApi = DoubanApi()
    # rsp = doubanApi.movie_detail(35460157)
    # logger.info(rsp.get('title'))

    # for i in range(1, 100):
    #     logger.info(i)
    #     rsp = doubanApi.movie_detail(35460157)
    #     logger.info(rsp.get('title'))
    #     if not rsp:
    #         logger.error("-------------------")

    #
    # sleep(round(random.uniform(2, 6), 1))
    # rsp = doubanApi.movie_top250()
    # i = 1
    # for item in rsp['subject_collection_items']:
    #     print('-------------------------------')
    #     print(i)
    #     doubanId = item['id']
    #     print(doubanId)
    #     sleep(round(random.uniform(2, 6), 1))
    #     detail = doubanApi.movie_detail(doubanId)
    #     if detail:
    #         print(detail['title'])
    #         print(detail['year'])
    #         print(detail['type'])
    #     i += 1
    #     print(item)

    # douban = Douban(config)
    # media_list = douban.get_douban_movies()
    # for media in media_list:
    #     print(media)
    # media = douban.get_media_detail_from_web("https://movie.douban.com/subject/35101436/")
    # print(media)
    # media = douban.get_media_detail_from_web("https://movie.douban.com/subject/34477861/")
    # print(media)

    # tmdb = Tmdb(config)
    # media = Media()
    # media.title = '大江大河2'
    # media.year = 2020
    # media.media_type = MediaType.TV
    # x = tmdb.match_tmdb(media)
    # logger.info(x)

    # rsp = tmdb.movie_detail(278)
    # logger.info(rsp)
    # rsp = tmdb.search_movie('流浪地球', 2019)
    # logger.info(rsp)
    # if len(rsp.get('results')) == 1:
    #     tmdb_id = rsp.get('results')[0]['id']
    #     rsp = tmdb.movie_detail(tmdb_id)
    #     logger.info(rsp)
    # rsp = tmdb.search_tv('成瘾剂量', 2021)
    # logger.info(rsp)
    # if len(rsp.get('results')) == 1:
    #     tmdb_id = rsp.get('results')[0]['id']
    #     rsp = tmdb.tv_detail(tmdb_id)
    #     logger.info(rsp)

    # imdb = Imdb(config)
    # imdb_ids = imdb.imdb_top250()
    # logger.info(imdb_ids)

    # media_db = MediaDb('../config')

    # print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # desired_ids = [1,2,3,4,5]
    # s = 'SELECT * FROM distro WHERE id IN (%s)' % ','.join('?'*len(desired_ids)), desired_ids
    # print(s)

    # douban = Douban(config)
    # douban_ids = douban.get_douban_movies()
    # logger.info(douban_ids)

    # radarr = Radarr(config)
    # rsp = radarr.lookup_movie_by_tmdb(278)
    # logger.debug(rsp)

    # sonarr = Sonarr(config)
    # rsp = sonarr.get_series()
    # logger.info(rsp)

    # title = '西部世界 第十二季'
    # pattern = r'[第\s]+([0-9一二三四五六七八九十S\-]+)\s*季'
    # rst = re.search(r'%s' % pattern, title, re.I)
    # logger.info(rst)
    # logger.info(rst.group())
    # logger.info(rst.group(0))
    # logger.info(rst.group(1))
    # season = rst.group(1)
    # season = cn2an(inputs=season, mode='smart')
    # logger.info(season)
    # title = title.rstrip(rst.group(0))
    # logger.info(title)
    #
    # c=3
    # d = { 'a': 1, 'b': 2}
    # d.update(c=c)
    # logger.info(d)

    # title = '大江大河22'
    # pattern = r'(.*?)(\d+)'
    # rst = re.search(r'%s' % pattern, title, re.I)
    # logger.info(rst)
    # logger.info(rst.group())
    # logger.info(rst.group(0))
    # logger.info(rst.group(1))
    # season = rst.group(1)
    # season = rst.group(2)
    # print(season)
    # logger.info(season)
    # title = title.rstrip(rst.group(0))
    # logger.info(title)

    # schedule.every(2).minutes.at(':10').do(run_job, 'xxx')
    # schedule.every(2).minutes.at(':20').do(run_job, 'zzz')

    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

    # fp = NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.json', prefix='wechat', delete=False)

    # emby = Emby(config)
    # rsp = emby.search_playlist('IMDB TOP250')
    # for pl in rsp.get('Items'):
    #     playlist_id = pl.get('Id')
    #     print(playlist_id)

    # imdb = Imdb(config)
    # imdb_ids = imdb.imdb_top250()
    # print(imdb_ids)

    # 从数据库查询最新的 豆瓣 TOP250 信息
    medias = SqlHelper.select_douban_top250()
    emby_ids = []
    for media in medias:
        if media.emby_id:
            emby_ids.append(media.emby_id)
    emby = Emby(config)
    rsp = emby.search_playlist('IMDB TOP250')
    # logger.info(rsp)
    if rsp and len(rsp.get('Items')) > 0:
        playlist_id = rsp.get('Items')[0]['Id']
        items = emby.get_playlist_items(playlist_id)
        # logger.info(items)
        if items and len(items.get('Items')) > 0:
            item_ids = [item.get('PlaylistItemId') for item in items.get('Items')]
            emby.remove_playlist_items(playlist_id, item_ids)
            # emby.add_playlist_items(playlist_id, emby_ids)
    else:
        emby.create_playlist('豆瓣 TOP250', emby_ids)
