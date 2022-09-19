import datetime
import logging
import random
from time import sleep

import requests
from lxml import etree
from requests.utils import dict_from_cookiejar

from app.douban import DoubanApi
from app.media import Media
from app.types import MediaType
from app.utils import RequestUtils


class Douban(object):

    logger = None
    users = []
    days = None
    types = None
    cookie = None
    requests = None
    doubanapi = None

    def __init__(self, config) -> None:
        self.logger = logging.getLogger(__name__)
        # 用户列表
        users = config.get('douban').get('users')
        if users:
            if not isinstance(users, list):
                users = [users]
            self.users = users
        # 时间范围
        self.days = int(config.get('douban').get('days')) if str(config.get('douban').get('days')).isdigit() else None
        # 类型
        types = config.get('douban').get('types')
        if types:
            self.types = types
        # Cookie
        cookie = config.get('douban').get('cookie')
        if not cookie:
            try:
                req = RequestUtils()
                rsp = req.get("https://www.douban.com/")
                if rsp:
                    cookie = dict_from_cookiejar(rsp.cookies)
            except Exception as err:
                self.logger.warning(f"[DouBan] 获取cookie失败：{format(err)}")
        self.requests = RequestUtils(cookies=cookie, session=requests.Session())
        self.doubanapi = DoubanApi()

    def douban2media(self, douban_id):
        """
        查询豆瓣详情，并组装媒体信息
        :param douban_ids:
        :return:
        """
        # 查询豆瓣详情
        self.logger.info(f'[DouBan] 正在查询豆瓣详情：{douban_id}')
        get_from_web = False
        max_retries = 10
        fail_count = 0
        while fail_count < max_retries:
            douban_info = self.doubanapi.movie_detail(douban_id)
            # 随机休眠
            sleep(round(random.uniform(3, 6), 1))
            if not douban_info:
                douban_info = self.doubanapi.tv_detail(douban_id)
                # 随机休眠
                sleep(round(random.uniform(3, 6), 1))
            if not douban_info:
                fail_count += 1
                self.logger.warning(f'第{fail_count}次获取豆瓣信息失败，将重试，最多10次')
                # 随机休眠
                sleep(round(random.uniform(60, 70), 1))
                continue
            break
        if not douban_info:
            self.logger.warning(f'[DouBan] %s 未从API找到豆瓣详细信息 {douban_id}, 尝试从web获取')
            get_from_web = True
        if douban_info.get("localized_message"):
            localized_message = douban_info.get("localized_message")
            self.logger.warning(f'[DouBan] 查询豆瓣详情返回：{localized_message}， 尝试从web获取')
            get_from_web = True
        if get_from_web:
            douban_info = self.media_detail_from_web(f'https://movie.douban.com/subject/{douban_id}/')
            # 随机休眠
            sleep(round(random.uniform(3, 6), 1))
            if not douban_info:
                self.logger.warning(f'[DouBan] %s 无权限访问，需要配置豆瓣Cookie {douban_id}')
        if not douban_info:
            self.logger.warning(f'[DouBan] %s 未找到豆瓣详细信息 {douban_id}')
            return
        # 组装媒体信息
        if douban_info.get('type'):
            media_type = MediaType.TV if douban_info.get('type') == 'tv' else MediaType.MOVIE
        else:
            media_type = MediaType.TV if douban_info.get("episodes_count") else MediaType.MOVIE
        media = Media()
        media.title = douban_info.get('title')
        media.year = douban_info.get('year')
        media.douban_id = douban_id
        media.media_type = media_type
        media.status = 'new'
        self.logger.info(f'[DouBan] {media_type.value}：{media.title} {media.year}'.strip())
        return media

    def douban_top250(self):
        """
        获取豆瓣 TOP250电影信息
        :return: 检索到的媒体信息列表（不含TMDB信息）
        """
        douban_ids = []
        rsp = self.doubanapi.movie_top250()
        # 随机休眠
        sleep(round(random.uniform(3, 6), 1))
        # self.logger.debug(rsp)
        if not rsp:
            self.logger.warning('[DouBan] 获取豆瓣 TOP250信息失败')
        for douban in rsp.get('subject_collection_items'):
            douban_id = douban.get('id')
            douban_ids.append(douban_id)
        return douban_ids

    def get_douban_movies(self):
        """
        获取每一个用户的每一个类型的豆瓣标记
        :return: 检索到的媒体信息列表（不含TMDB信息）
        """
        if not self.days or not self.users or not self.types:
            self.logger.warning("[DouBan] 豆瓣未配置或配置不正确")
            return []
        # 豆瓣ID列表
        douban_ids = []
        # 开始序号
        start_num = 0
        # 每页条数
        per_page_num = 15
        # 每一个用户
        for user in self.users:
            if not user:
                continue
            # 每一个类型成功数量
            user_success_num = 0
            for mtype in self.types:
                if not mtype:
                    continue
                self.logger.info(f"[DouBan] 开始获取 {user} 的 {mtype} 数据...")
                # 类型成功数量
                user_type_success_num = 0
                # 每一页
                while True:
                    # 页数
                    page_number = int(start_num / per_page_num + 1)
                    # 当前页成功数量
                    url_success_num = 0
                    # 是否继续下一页
                    continue_next_page = True
                    self.logger.debug(f"[DouBan] 开始解析第 {page_number} 页数据...")
                    try:
                        # 解析豆瓣页面
                        url = f"https://movie.douban.com/people/{user}/{mtype}"
                        params = {
                            'start': start_num,
                            'sort': 'time',
                            'rating': 'all',
                            'filter': 'all',
                            'mode': 'grid'
                        }
                        res = self.requests.get(url=url, params=params)
                        if not res:
                            self.logger.warning(f"[DouBan] 第 {page_number} 页无法访问")
                            break
                        html_text = res.text
                        if not html_text:
                            self.logger.warning(f"[DouBan] 第 {page_number} 页未获取到数据")
                            break
                        html = etree.HTML(html_text)
                        # ID列表
                        items = html.xpath(
                            "//div[@class='info']//a[contains(@href,'https://movie.douban.com/subject/')]/@href")
                        if not items:
                            break
                        # 时间列表
                        dates = html.xpath("//div[@class='info']//span[@class='date']/text()")
                        if not dates:
                            break
                        # 计算当前页有效个数
                        items_count = 0
                        for date in dates:
                            mark_date = datetime.datetime.strptime(date, '%Y-%m-%d')
                            if (datetime.datetime.now() - mark_date).days < int(self.days):
                                items_count += 1
                            else:
                                break
                        # 当前页有效个数不足15个时
                        if items_count < 15:
                            continue_next_page = False
                        # 解析豆瓣ID
                        for item in items:
                            items_count -= 1
                            if items_count < 0:
                                break
                            douban_id = item.split("/")[-2]
                            if str(douban_id).isdigit() and douban_id not in douban_ids:
                                self.logger.info(f'[DouBan] 解析到媒体：{douban_id}')
                                douban_ids.append(douban_id)
                                url_success_num += 1
                                user_type_success_num += 1
                                user_success_num += 1
                        self.logger.debug(f'[DouBan] 第 {page_number} 页解析完成，共获取到 {url_success_num} 个媒体')
                    except Exception as err:
                        self.logger.error(f'[DouBan] 第 {page_number} 页解析出错：%s' % str(err))
                        break
                    # 继续下一页
                    if continue_next_page:
                        start_num += per_page_num
                        # 随机休眠
                        sleep(round(random.uniform(1, 3), 1))
                    else:
                        break
                # 当前类型解析结束
                self.logger.debug(f"[DouBan] 用户 {user} 的 {mtype} 解析完成，共获取到 {user_type_success_num} 个媒体")
            # 当解析用户结束
            self.logger.info(f"[DouBan] 用户 {user} 解析完成，共获取到 {user_success_num} 个媒体")
        # 当所有解析结束
        self.logger.info(f"[DouBan] 所有用户解析完成，共获取到 {len(douban_ids)} 个媒体")
        # 随机休眠
        sleep(round(random.uniform(3, 6), 1))
        return douban_ids

    def media_detail_from_web(self, url):
        """
        从豆瓣详情页抓紧媒体信息
        :param url: 豆瓣详情页URL
        :return: {title, year, intro, cover_url, rating{value}, episodes_count}
        """
        ret_media = {}
        rsp = self.requests.get(url=url)
        if rsp and rsp.status_code == 200:
            html_text = rsp.text
            if not html_text:
                return None
            try:
                html = etree.HTML(html_text)
                ret_media['title'] = html.xpath("//span[@property='v:itemreviewed']/text()")[0]
                if not ret_media.get('title'):
                    return None
                ret_media['year'] = html.xpath("//div[@id='content']//span[@class='year']/text()")[0][1:-1]
                detail_info = html.xpath("//div[@id='info']/text()")
                if isinstance(detail_info, list):
                    detail_info = [str(x).strip() for x in detail_info if str(x).strip().isdigit()]
                    if detail_info and str(detail_info[0]).isdigit():
                        ret_media['episodes_count'] = int(detail_info[0])
            except Exception as err:
                print(err)
        return ret_media
