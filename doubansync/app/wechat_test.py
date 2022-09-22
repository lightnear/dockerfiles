# -*- coding: utf-8 -*-
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='douban sync')
    parser.add_argument('-c', '--config', default="../config/config.yml", help='config file')
    args = parser.parse_args()
    config_file = args.config
    config = load_config(config_file)
    config_path, _ = os.path.split(config_file)
    os.environ['DB_CONFIG_PATH'] = os.path.abspath(config_path)
    # logger.debug(config)

    wechat = Wechat()
    # wechat.send_text('aa', touser='lightnear')
    # wechat.send_image(r'C:\Users\lightnear\Downloads\11.jpg', touser='lightnear')
    # wechat.send_video(r'C:\Users\lightnear\Downloads\11.mp4', touser='lightnear')
    # wechat.upload_p_image(r'C:\Users\lightnear\Downloads\11.jpg')
    #     wechat.send_textcard('新的起点',
    #                          '''监控ID:47218
    # 告警主机:pf.faye.cool
    # 告警主机:10.1.1.1
    # 告警时间:2022.09.21 05:10:04
    # 告警等级:Average
    # 告警信息: PFSense: Link down
    # 告警项目:net.if.status[9]
    # 问题详情:PFSense: Interface [pppoe0(WAN)]: Operational status:dormant (5)
    # 当前状态:OK:dormant (5)
    # 事件ID:180790''',
    #                          'https://dataworld.fun',
    #                          touser='lightnear')

    # wechat.send_news('父母爱情',
    #                  r'要放在解放前，江德福（郭涛 饰）和安杰（梅婷 饰）这对男女可真是八竿子够不上关系的两个人。他们一个是年轻有为、干练果敢的海军军官，一个是从小养尊处优、娇媚华贵的资本家小姐，但20世纪50年代的沧桑巨变让他们俩人走到了一起。江德福在舞会上结识美丽的安杰，虽然他冒冒失失，又 是个目不识丁的大老粗，经过一番周折他们终于组建了成分不相匹配的小家庭。问题是不相匹配的何止是出身，还有各自的阅历、学历以及人生态度，在之后的岁月里，他们打打闹闹，吵架拌嘴，俨然成了家庭常态，更有江德华（刘琳 饰）这类人物从中加油添醋。',
    #                  'https://movie.douban.com/subject/19965220/?_dtcc=1',
    #                  'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2554351588.webp',
    #                  touser='lightnear')

    wechat.send_mpnews(
        '父母爱情',
        r'要放在解放前，江德福（郭涛 饰）和安杰（梅婷 饰）这对男女可真是八竿子够不上关系的两个人。他们一个是年轻有为、干练果敢的海军军官，一个是从小养尊处优、娇媚华贵的资本家小姐，但20世纪50年代的沧桑巨变让他们俩人走到了一起。江德福在舞会上结识美丽的安杰，虽然他冒冒失失，又 是个目不识丁的大老粗，经过一番周折他们终于组建了成分不相匹配的小家庭。问题是不相匹配的何止是出身，还有各自的阅历、学历以及人生态度，在之后的岁月里，他们打打闹闹，吵架拌嘴，俨然成了家庭常态，更有江德华（刘琳 饰）这类人物从中加油添醋。',
        '32MBOnSwDPnUb3IKTCTOuFEAiwCW5FzE42mKNAalGeiWwPbuZygN3MVnW7x-dDVPI',
        """
        <div style="text-align: center;">
        <img src='https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2554351588.webp'>
        </div>
<section class="subject-desc"><h1>影片信息</h1><table><tbody><tr><td>片名</td><td>父母爱情</td></tr><tr><td>又名</td><td>RomanceofOurParents/ParentsLove</td></tr><tr><td>导演</td><td>孔笙</td></tr><tr><td>编剧</td><td>刘静</td></tr><tr><td>主演</td><td>郭涛/梅婷/刘琳/任帅/刘奕君/张延/郭广平/王菁华/娜仁花/毕彦君/贾延鹏/关晓彤/方慧/黄诗佳/张陆/张龄心/杨立新/刘天池/刘敏涛/王永泉/赵千紫/杨司晨/崔明浩/石云鹏/柳明明/张娇娇/陈雅熙/张乐昊旻/彭婧/张琛/李金江/赵一龙/郭鹏/李超/王宏/张昕琦/张昕瑶/柳欣言/战鹤文/陈旭/黄海/张九妹/林龙麒/王丹彤/王天泽/李小川/吕添尧/刘凌志/杨晓丹/张元戎/黄岗/王仪伟/傅晓娜/兰娟/阚博/蒋雯丽/杨心仪/江昊桐</td></tr><tr><td>播出</td><td>央视一套/江苏卫视</td></tr><tr><td>首播</td><td>2014-02-02(中国大陆)</td></tr><tr><td>类型</td><td>爱情/家庭</td></tr><tr><td>集数</td><td>44</td></tr><tr><td>每集</td><td>45分钟</td></tr><tr><td>地区</td><td>中国大陆</td></tr><tr><td>语言</td><td>汉语普通话</td></tr><tr><td>IMDb</td><td>tt4168486</td>
</tr></tbody></table></section>
<style> .subject-desc{color:#494949;font-size:15px;padding:20px}.subject-desc a{color:#3BA94D}.subject-desc h1{font-size:25px;font-weight:500;margin:0 0 20px;color:#494949}.subject-desc table{border-spacing:0}.subject-desc td:first-child{color:#9B9B9B;white-space:nowrap;vertical-align:top}.subject-desc td:first-child:after{content:":"} </style>
<section class="subject-desc">
<h1>简介</h1>
<hr>
要放在解放前，江德福（郭涛 饰）和安杰（梅婷 饰）这对男女可真是八竿子够不上关系的两个人。他们一个是年轻有为、干练果敢的海军军官，一个是从小养尊处优、娇媚华贵的资本家小姐，但20世纪50年代的沧桑巨变让他们俩人走到了一起。江德福在舞会上结识美丽的安杰，虽然他冒冒失失，又 是个目不识丁的大老粗，经过一番周折他们终于组建了成分不相匹配的小家庭。问题是不相匹配的何止是出身，还有各自的阅历、学历以及人生态度，在之后的岁月里，他们打打闹闹，吵架拌嘴，俨然成了家庭常态，更有江德华（刘琳 饰）这类人物从中加油添醋。<br>这是父辈们平常而又有些特殊的典型案例，将他们紧紧锁在一起的不仅仅是爱情，更有……
</section>
""",
        touser='lightnear')




"""
        <div style="text-align: center;">
        <img src='https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2554351588.webp'>
        </div>
<section class="subject-desc"><h1>影片信息</h1><table><tbody><tr><td>片名</td><td>父母爱情</td></tr><tr><td>又名</td><td>RomanceofOurParents/ParentsLove</td></tr><tr><td>导演</td><td>孔笙</td></tr><tr><td>编剧</td><td>刘静</td></tr><tr><td>主演</td><td>郭涛/梅婷/刘琳/任帅/刘奕君/张延/郭广平/王菁华/娜仁花/毕彦君/贾延鹏/关晓彤/方慧/黄诗佳/张陆/张龄心/杨立新/刘天池/刘敏涛/王永泉/赵千紫/杨司晨/崔明浩/石云鹏/柳明明/张娇娇/陈雅熙/张乐昊旻/彭婧/张琛/李金江/赵一龙/郭鹏/李超/王宏/张昕琦/张昕瑶/柳欣言/战鹤文/陈旭/黄海/张九妹/林龙麒/王丹彤/王天泽/李小川/吕添尧/刘凌志/杨晓丹/张元戎/黄岗/王仪伟/傅晓娜/兰娟/阚博/蒋雯丽/杨心仪/江昊桐</td></tr><tr><td>播出</td><td>央视一套/江苏卫视</td></tr><tr><td>首播</td><td>2014-02-02(中国大陆)</td></tr><tr><td>类型</td><td>爱情/家庭</td></tr><tr><td>集数</td><td>44</td></tr><tr><td>每集</td><td>45分钟</td></tr><tr><td>地区</td><td>中国大陆</td></tr><tr><td>语言</td><td>汉语普通话</td></tr><tr><td>IMDb</td><td>tt4168486</td>
</tr></tbody></table></section>
<style> .subject-desc{color:#494949;font-size:15px;padding:20px}.subject-desc a{color:#3BA94D}.subject-desc h1{font-size:25px;font-weight:500;margin:0 0 20px;color:#494949}.subject-desc table{border-spacing:0}.subject-desc td:first-child{color:#9B9B9B;white-space:nowrap;vertical-align:top}.subject-desc td:first-child:after{content:":"} </style>
<section class="subject-desc">
<h1>简介</h1>
<hr>
要放在解放前，江德福（郭涛 饰）和安杰（梅婷 饰）这对男女可真是八竿子够不上关系的两个人。他们一个是年轻有为、干练果敢的海军军官，一个是从小养尊处优、娇媚华贵的资本家小姐，但20世纪50年代的沧桑巨变让他们俩人走到了一起。江德福在舞会上结识美丽的安杰，虽然他冒冒失失，又 是个目不识丁的大老粗，经过一番周折他们终于组建了成分不相匹配的小家庭。问题是不相匹配的何止是出身，还有各自的阅历、学历以及人生态度，在之后的岁月里，他们打打闹闹，吵架拌嘴，俨然成了家庭常态，更有江德华（刘琳 饰）这类人物从中加油添醋。<br>这是父辈们平常而又有些特殊的典型案例，将他们紧紧锁在一起的不仅仅是爱情，更有……
</section>
"""
