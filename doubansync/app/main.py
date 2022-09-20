# -*- coding: UTF-8 -*-
import os
import sys
import datetime
import schedule
import time
import logging
import logging.config
import yaml
import argparse

sys.path.append(os.path.abspath('..'))

from app.db import SqlHelper
from app.douban import Douban
from app.emby import Emby
from app.imdb import Imdb
from app.radarr import Radarr
from app.sonarr import Sonarr
from app.tmdb import Tmdb
from app.utils import MediaType
from app.wechat import Wechat

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


def douban_top250(config) -> None:
    logger.info('开始同步豆瓣 TOP250')
    message = ""
    # 更新 豆瓣 TOP250 信息到数据库
    douban = Douban(config)
    tmdb = Tmdb(config)
    douban_ids = douban.douban_top250()
    if not douban_ids:
        logger.info('未获取到 豆瓣 TOP250 列表')
        return
    rank = 0
    for douban_id in douban_ids:
        rank += 1
        media = SqlHelper.select_media_by_douban(douban_id)
        if media:
            media.douban_rank = rank
            media.update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            SqlHelper.update_media(media)
        else:
            douban_info = douban.get_douban_info(douban_id)
            if not douban_info:
                logger.warning(f'未找到豆瓣详情 {douban_id}')
                continue
            media = douban.douban2media(douban_info)
            media = tmdb.match_tmdb(media)
            if not media:
                logger.warning(f'未匹配到TMDB信息 {media.media_type.value} {media.title} {media.year}')
                continue
            if media.tmdb_id:
                db_media = SqlHelper.select_media_by_tmdb(media.tmdb_id)
            elif media.tvdb_id:
                db_media = SqlHelper.select_media_by_tvdb(media.tvdb_id)
            if db_media:
                db_media.douban_id = media.douban_id
                db_media.douban_rank = rank
                db_media.update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                SqlHelper.update_media(db_media)
            else:
                media.status = 'wait'
                media.douban_rank = rank
                SqlHelper.save_media(media)
    SqlHelper.update_douban_ranks(douban_ids)

    # 添加到 radarr
    add_medias(config)

    # 同步 emby 信息
    sync_emby(config)

    # 从数据库查询最新的 豆瓣 TOP250 信息
    medias = SqlHelper.select_douban_top250()
    emby_ids = []
    for media in medias:
        if media.emby_id:
            emby_ids.append(media.emby_id)

    # 创建 emby 播放列表
    create_emby_playlist(config, '豆瓣 TOP250', emby_ids)

    # 发送消息
    if message:
        wechat = Wechat(config)
        to = '@all'
        subject = 'douban top 250'
        wechat.send_message(subject, message, to)
    logger.info('完成同步豆瓣 TOP250')


def imdb_top250(config) -> None:
    logger.info('开始同步IMDB TOP250')
    message = ""
    # 更新 豆瓣 TOP250 信息到数据库
    imdb = Imdb(config)
    radarr = Radarr(config)
    imdb_ids = imdb.imdb_top250()
    if not imdb_ids:
        logger.info('未获取到 IMDB TOP250 列表')
        return
    rank = 0
    for imdb_id in imdb_ids:
        rank += 1
        media = SqlHelper.select_media_by_imdb(imdb_id)
        if media:
            media.imdb_rank = rank
            media.update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            SqlHelper.update_media(media)
        else:
            media = radarr.imdb2media(imdb_id)
            if media.tmdb_id:
                db_media = SqlHelper.select_media_by_tmdb(media.tmdb_id)
            elif media.tvdb_id:
                db_media = SqlHelper.select_media_by_tvdb(media.tvdb_id)
            if db_media:
                db_media.imdb_id = media.imdb_id
                db_media.imdb_rank = rank
                SqlHelper.update_media(db_media)
            else:
                media.imdb_rank = rank
                media.status = 'wait'
                SqlHelper.save_media(media)
    SqlHelper.update_imdb_ranks(imdb_ids)

    # 添加到 radarr
    add_medias(config)

    # 同步 emby 信息
    sync_emby(config)

    # 从数据库查询最新的 IMDB TOP250 信息
    medias = SqlHelper.select_imdb_top250()
    emby_ids = []
    for media in medias:
        if media.emby_id:
            emby_ids.append(media.emby_id)

    # 创建 emby 播放列表
    create_emby_playlist(config, 'IMDB TOP250', emby_ids)

    # 发送消息
    if message:
        wechat = Wechat(config)
        to = '@all'
        subject = 'imdb top 250'
        wechat.send_message(subject, message, to)
    logger.info('完成同步IMDB TOP250')


def create_emby_playlist(config, name, emby_ids: list):
    emby = Emby(config)
    rsp = emby.search_playlist(name)
    if rsp and len(rsp.get('Items')) > 0:
        playlist_id = rsp.get('Items')[0]['Id']
        items = emby.get_playlist_items(playlist_id)
        if items and len(rsp.get('Items')) > 0:
            item_ids = [item.get('PlaylistItemId') for item in items.get('Items')]
            emby.remove_playlist_items(playlist_id, item_ids)
            emby.add_playlist_items(playlist_id, emby_ids)
    else:
        emby.create_playlist(name, emby_ids)


def run_douban(config) -> None:
    logger.info('开始同步豆瓣想看列表')
    message = ""
    douban = Douban(config)
    tmdb = Tmdb(config)
    douban_ids = douban.get_douban_movies()
    if not douban_ids:
        logger.info('没有新增的豆瓣内容')
        return
    for douban_id in douban_ids:
        media = SqlHelper.select_media_by_douban(douban_id)
        if media:
            # media.update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            SqlHelper.update_media(media)
            logger.info(f'数据库中已存在影视: {media.media_type.value} {media.title} {media.year}')
        else:
            douban_info = douban.get_douban_info(douban_id)
            if not douban_info:
                logger.warning(f'未找到豆瓣详情 {douban_id}')
                continue
            media = douban.douban2media(douban_info)
            media = tmdb.match_tmdb(media)
            if not media:
                logger.warning(f'未匹配到TMDB信息 {media.media_type.value} {media.title} {media.year}')
                continue
            if media.tmdb_id:
                db_media = SqlHelper.select_media_by_tmdb(media.tmdb_id)
            elif media.tvdb_id:
                db_media = SqlHelper.select_media_by_tvdb(media.tvdb_id)
            if db_media:
                db_media.douban_id = media.douban_id
                db_media.tmdb_id = media.tmdb_id
                db_media.tvdb_id = media.tvdb_id
                db_media.imdb_id = media.imdb_id
                db_media.update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                SqlHelper.update_media(db_media)
                logger.info(f'数据库中已存在影视: {db_media.media_type.value} {db_media.title} {db_media.year}')
            else:
                media.status = 'wait'
                SqlHelper.save_media(media)
                logger.info(f'从豆瓣列表中找到新影视: {media.media_type.value} {media.title} {media.year}')
                message += f'{media.media_type.value} {media.title} {media.year}\n'

    # 发送消息
    if message:
        wechat = Wechat(config)
        to = '@all'
        subject = '从豆瓣列表中找到新影视'
        wechat.send_message(subject, message, to)
    logger.info('完成同步豆瓣想看列表')


def add_medias(config):
    """
    添加影视到 radarr sonarr
    :param config:
    :return:
    """
    logger.info('开始同步PMR信息')
    message = ""
    radarr = Radarr(config)
    sonarr = Sonarr(config)
    medias = SqlHelper.search_medias_by_status('wait')
    if not medias:
        logger.info('没有媒体需要添加')
        return
    for media in medias:
        logger.info(f'开始添加 {media.media_type.value} {media.title} {media.year}')
        if media.media_type == MediaType.MOVIE and media.tmdb_id:
            if radarr.get_movie_by_tmdb(media.tmdb_id):
                media.status = 'add'
                SqlHelper.update_media(media)
                logger.info(f'电影在PMR中已存在：{media.media_type.value} {media.title} {media.year}')
            else:
                rsp = radarr.add_movie(media)
                if rsp:
                    media.status = 'add'
                    SqlHelper.update_media(media)
                    logger.info(f'添加电影成功，将自动搜索下载：{media.media_type.value} {media.title} {media.year}')
                    message += f'成功：{media.media_type.value} {media.title} {media.year}\n'
                else:
                    logger.info(f'添加电影失败：{media.media_type.value} {media.title} {media.year}')
                    message += f'失败: {media.media_type.value} {media.title} {media.year}\n'
        if media.media_type == MediaType.TV and media.tvdb_id:
            sonarr_series = sonarr.get_series()
            sonarr_series_ids = [series.get('tvdbId') for series in sonarr_series]
            if media.tvdb_id in sonarr_series_ids:
                media.status = 'add'
                SqlHelper.update_media(media)
                logger.info(f'电视剧在PMR中已存在：{media.media_type.value} {media.title} {media.year}')
            else:
                rsp = sonarr.add_series(media)
                if rsp:
                    media.status = 'add'
                    SqlHelper.update_media(media)
                    logger.info(f'添加电视剧成功，将自动搜索下载：{media.media_type.value} {media.title} {media.year}')
                    message += f'成功：{media.media_type.value} {media.title} {media.year}\n'
                else:
                    logger.info(f'添加电视剧失败：{media.media_type.value} {media.title} {media.year}')
                    message += f'失败：{media.media_type.value} {media.title} {media.year}\n'
    # 发送消息
    if message:
        wechat = Wechat(config)
        to = '@all'
        subject = '添加影视，将自动搜索下载'
        wechat.send_message(subject, message, to)
    logger.info('完成同步PMR信息')


def sync_emby(config):
    """
    数据库中的影视同步 emby 信息
    :param config:
    :return:
    """
    logger.info('开始同步Emby信息')
    message = ""
    emby = Emby(config)
    medias = SqlHelper.search_medias_by_status('add')
    if not medias:
        logger.info('没有媒体需要同步')
        return
    for media in medias:
        logger.info(f'同步媒体 {media.media_type.value} {media.title} {media.year}')
        if media.media_type == MediaType.MOVIE:
            emby_item = emby.search_movie_by_tmdb(media.tmdb_id)
        if media.media_type == MediaType.TV:
            emby_item = emby.search_series_by_tvdb(media.tvdb_id)

        if emby_item and emby_item.get('TotalRecordCount') > 0:
            media.emby_id = emby_item.get('Items')[0]['Id']
            media.status = 'finish'
            media.sync_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            SqlHelper.update_media(media)
            logger.info(f'媒体库有新的影视剧，可以看了: {media.media_type.value} {media.title} {media.year}')
            message += f'{media.media_type.value} {media.title} {media.year}\n'
        else:
            logger.info(f'媒体尚未下载完成 {media.media_type.value} {media.title} {media.year}')

    # 发送消息
    if message:
        wechat = Wechat(config)
        to = '@all'
        subject = '媒体库有新的影视剧，可以看了'
        wechat.send_message(subject, message, to)
    logger.info('完成同步Emby信息')


# 运行
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='douban sync')
    parser.add_argument('-c', '--config', default="/config/config.yml", help='config file')
    args = parser.parse_args()
    config_file = args.config
    config = load_config(config_file)
    config_path, _ = os.path.split(config_file)
    os.environ['DB_CONFIG_PATH'] = os.path.abspath(config_path)

    douban_top250(config)
    imdb_top250(config)
    run_douban(config)
    add_medias(config)
    sync_emby(config)

    schedule.every(config.get('schedule').get('douban')).minutes.do(run_douban, config)  # 每小时同步一次 豆瓣想看列表
    schedule.every(config.get('schedule').get('sync')).minutes.do(add_medias, config)  # 每10min同步一次 添加至PMR
    schedule.every(config.get('schedule').get('sync')).minutes.do(sync_emby, config)   # 每10min同步一次 同步EMBY
    schedule.every(config.get('schedule').get('imdb_top250')).hours.at(':15').do(imdb_top250, config)  # IMDB TOP250
    schedule.every(config.get('schedule').get('douban_top250')).hours.at(':45').do(douban_top250, config)  # 豆瓣 TOP250
    while True:
        schedule.run_pending()
        time.sleep(1)
