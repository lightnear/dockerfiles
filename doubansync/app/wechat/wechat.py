import logging
import os

import yaml

from .wechatApi import WeChatApi
from .wechatHandler import WechatHandler


class Wechat(WeChatApi):

    def __init__(self, config=None) -> None:
        self.logger = logging.getLogger(__name__)
        config_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '.wechat.config.yml')
        print(config_file)
        if config:
            self.corpid = config.get('wechat').get('corpid')
            self.corpsecret = config.get('wechat').get('corpsecret')
            self.agentid = config.get('wechat').get('agentid')
            self.base_url = config.get('wechat').get('base_url')
        elif os.path.isfile(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as r:
                    config = yaml.safe_load(r)
                    self.corpid = config.get('wechat').get('corpid')
                    self.corpsecret = config.get('wechat').get('corpsecret')
                    self.agentid = config.get('wechat').get('agentid')
                    self.base_url = config.get('wechat').get('base_url')
            except Exception as e:
                self.logger.warning(f'读取配置文件失败: {str(e)}')
        self.handler = WechatHandler(self.corpid, self.corpsecret, self.agentid, self.base_url)

    def send_text(self,
                  content,
                  touser=None,
                  toparty=None,
                  totag=None,
                  safe=0,
                  enable_duplicate_check=0,
                  duplicate_check_interval=1800,
                  **kwargs):
        """
        发送文本消息
        :param content: 消息内容
        :param touser: 指定接收消息的成员，成员ID列表（多个接收者用‘|’分隔，最多支持1000个）。特殊情况：指定为"@all"，则向该企业应用的全部成员发送
        :param toparty: 指定接收消息的部门，部门ID列表，多个接收者用‘|’分隔，最多支持100个。当touser为"@all"时忽略本参数
        :param totag: 指定接收消息的标签，标签ID列表，多个接收者用‘|’分隔，最多支持100个。当touser为"@all"时忽略本参数
        :param safe: 表示是否是保密消息，0表示可对外分享，1表示不能分享且内容显示水印，默认为0
        :param enable_duplicate_check: 表示是否开启重复消息检查，0表示否，1表示是，默认0
        :param duplicate_check_interval: 表示是否重复消息检查的时间间隔，默认1800s，最大不超过4小时
        :param kwargs: 其它参数
        :return:
        """
        message = {
            'content': content
        }
        self.handler.send_message('text', message, touser, toparty, totag, safe, enable_duplicate_check,
                                  duplicate_check_interval, **kwargs)

    def send_image(self, image_path,
                   touser=None,
                   toparty=None,
                   totag=None,
                   safe=0,
                   enable_duplicate_check=0,
                   duplicate_check_interval=1800,
                   **kwargs):
        """
        发送图片消息，仅支持jpg,png格式，大小5B~10M
        :param image_path: 发送图片的本地路径
        :param touser: 指定接收消息的成员，成员ID列表（多个接收者用‘|’分隔，最多支持1000个）。特殊情况：指定为"@all"，则向该企业应用的全部成员发送
        :param toparty: 指定接收消息的部门，部门ID列表，多个接收者用‘|’分隔，最多支持100个。当touser为"@all"时忽略本参数
        :param totag: 指定接收消息的标签，标签ID列表，多个接收者用‘|’分隔，最多支持100个。当touser为"@all"时忽略本参数
        :param safe: 表示是否是保密消息，0表示可对外分享，1表示不能分享且内容显示水印，默认为0
        :param enable_duplicate_check: 表示是否开启重复消息检查，0表示否，1表示是，默认0
        :param duplicate_check_interval: 表示是否重复消息检查的时间间隔，默认1800s，最大不超过4小时
        :param kwargs: 其它参数
        """
        message = {'media_path': image_path}
        self.handler.send_message('image', message, touser, toparty, totag, safe, enable_duplicate_check,
                                  duplicate_check_interval, **kwargs)

    def send_voice(self, voice_path, touser=None,
                   toparty=None,
                   totag=None,
                   safe=0,
                   enable_duplicate_check=0,
                   duplicate_check_interval=1800, **kwargs):
        """
        发送语音消息，仅支持amr格式，大小5B~2M, 播放长度不超过60s
        :param voice_path: 发送语音文件的本地路径
        :param touser: 指定接收消息的成员，成员ID列表（多个接收者用‘|’分隔，最多支持1000个）。特殊情况：指定为"@all"，则向该企业应用的全部成员发送
        :param toparty: 指定接收消息的部门，部门ID列表，多个接收者用‘|’分隔，最多支持100个。当touser为"@all"时忽略本参数
        :param totag: 指定接收消息的标签，标签ID列表，多个接收者用‘|’分隔，最多支持100个。当touser为"@all"时忽略本参数
        :param safe: 表示是否是保密消息，0表示可对外分享，1表示不能分享且内容显示水印，默认为0
        :param enable_duplicate_check: 表示是否开启重复消息检查，0表示否，1表示是，默认0
        :param duplicate_check_interval: 表示是否重复消息检查的时间间隔，默认1800s，最大不超过4小时
        :param kwargs: 其它参数
        :return:
        """
        message = {'media_path': voice_path}
        self.handler.send_message('voice', message, touser, toparty, totag, safe, enable_duplicate_check,
                                  duplicate_check_interval, **kwargs)

    def send_video(self, video_path, title=None, desc=None, touser=None,
                   toparty=None,
                   totag=None,
                   safe=0,
                   enable_duplicate_check=0,
                   duplicate_check_interval=1800, **kwargs):
        """
        发送视频消息，仅支持MP4格式的视频消息，大小5B~10M
        :param video_path: 发送视频文件的本地路径
        :param title: 视频消息的标题，不超过128个字节，超过会自动截断.当不指定时默认为上传视频的文件名
        :param desc: 视频消息的描述，不超过512个字节，超过会自动截断
        :param touser: 指定接收消息的成员，成员ID列表（多个接收者用‘|’分隔，最多支持1000个）。特殊情况：指定为"@all"，则向该企业应用的全部成员发送
        :param toparty: 指定接收消息的部门，部门ID列表，多个接收者用‘|’分隔，最多支持100个。当touser为"@all"时忽略本参数
        :param totag: 指定接收消息的标签，标签ID列表，多个接收者用‘|’分隔，最多支持100个。当touser为"@all"时忽略本参数
        :param safe: 表示是否是保密消息，0表示可对外分享，1表示不能分享且内容显示水印，默认为0
        :param enable_duplicate_check: 表示是否开启重复消息检查，0表示否，1表示是，默认0
        :param duplicate_check_interval: 表示是否重复消息检查的时间间隔，默认1800s，最大不超过4小时
        :param kwargs: 其它参数
        :return:
        """
        message = {'media_path': video_path}

        if title:
            message['title'] = title

        if desc:
            message['description'] = desc

        self.handler.send_message('video', message, touser, toparty, totag, safe, enable_duplicate_check,
                                  duplicate_check_interval, **kwargs)

    def send_file(self, file_path, touser=None,
                  toparty=None,
                  totag=None,
                  safe=0,
                  enable_duplicate_check=0,
                  duplicate_check_interval=1800, **kwargs):
        """
        发送文件消息, 大小5B~10M
        :param file_path: 发送文件的本地路径
        :param touser: 指定接收消息的成员，成员ID列表（多个接收者用‘|’分隔，最多支持1000个）。特殊情况：指定为"@all"，则向该企业应用的全部成员发送
        :param toparty: 指定接收消息的部门，部门ID列表，多个接收者用‘|’分隔，最多支持100个。当touser为"@all"时忽略本参数
        :param totag: 指定接收消息的标签，标签ID列表，多个接收者用‘|’分隔，最多支持100个。当touser为"@all"时忽略本参数
        :param safe: 表示是否是保密消息，0表示可对外分享，1表示不能分享且内容显示水印，默认为0
        :param enable_duplicate_check: 表示是否开启重复消息检查，0表示否，1表示是，默认0
        :param duplicate_check_interval: 表示是否重复消息检查的时间间隔，默认1800s，最大不超过4小时
        :param kwargs: 其它参数
        :return:
        """
        message = {'media_path': file_path}
        self.handler.send_message('file', message, touser, toparty, totag, safe, enable_duplicate_check,
                                  duplicate_check_interval, **kwargs)

    def send_textcard(self, title, desc, url, btntxt="详情", touser=None,
                      toparty=None,
                      totag=None,
                      safe=0,
                      enable_duplicate_check=0,
                      duplicate_check_interval=1800, **kwargs):
        """
        发送文本卡片消息
        :param title: 标题，不超过128个字节，超过会自动截断（支持id转译）
        :param desc: 描述，不超过512个字节，超过会自动截断（支持id转译）
        :param url: 点击后跳转的链接。最长2048字节，请确保包含了协议头(http/https)
        :param btntxt: 按钮文字。 默认为“详情”， 不超过4个文字，超过自动截断。
        :param touser: 指定接收消息的成员，成员ID列表（多个接收者用‘|’分隔，最多支持1000个）。特殊情况：指定为"@all"，则向该企业应用的全部成员发送
        :param toparty: 指定接收消息的部门，部门ID列表，多个接收者用‘|’分隔，最多支持100个。当touser为"@all"时忽略本参数
        :param totag: 指定接收消息的标签，标签ID列表，多个接收者用‘|’分隔，最多支持100个。当touser为"@all"时忽略本参数
        :param safe: 表示是否是保密消息，0表示可对外分享，1表示不能分享且内容显示水印，默认为0
        :param enable_duplicate_check: 表示是否开启重复消息检查，0表示否，1表示是，默认0
        :param duplicate_check_interval: 表示是否重复消息检查的时间间隔，默认1800s，最大不超过4小时
        :param kwargs: 其它参数
        :return:
        """
        message = {'title': title, 'description': desc, 'url': url, 'btntxt': btntxt}
        self.handler.send_message('textcard', message, touser, toparty, totag, safe, enable_duplicate_check,
                                  duplicate_check_interval, **kwargs)

    def send_news(self, title, desc, url, pic_url, touser=None,
                  toparty=None,
                  totag=None,
                  safe=0,
                  enable_duplicate_check=0,
                  duplicate_check_interval=1800, **kwargs):
        """
        发送图文卡片消息
        :param title: 标题，不超过128个字节，超过会自动截断（支持id转译）
        :param desc:  描述，不超过512个字节，超过会自动截断（支持id转译）
        :param url:  点击后跳转的链接。 最长2048字节，请确保包含了协议头(http/https)
        :param pic_url: 图文消息的图片链接，最长2048字节，支持JPG、PNG格式，较好的效果为大图 1068*455，小图150*150。
        :param touser: 指定接收消息的成员，成员ID列表（多个接收者用‘|’分隔，最多支持1000个）。特殊情况：指定为"@all"，则向该企业应用的全部成员发送
        :param toparty: 指定接收消息的部门，部门ID列表，多个接收者用‘|’分隔，最多支持100个。当touser为"@all"时忽略本参数
        :param totag: 指定接收消息的标签，标签ID列表，多个接收者用‘|’分隔，最多支持100个。当touser为"@all"时忽略本参数
        :param safe: 表示是否是保密消息，0表示可对外分享，1表示不能分享且内容显示水印，默认为0
        :param enable_duplicate_check: 表示是否开启重复消息检查，0表示否，1表示是，默认0
        :param duplicate_check_interval: 表示是否重复消息检查的时间间隔，默认1800s，最大不超过4小时
        :param kwargs: 其它参数
        :return:
        """
        message = {'articles': [{'title': title, 'description': desc, 'url': url, 'picurl': pic_url}]}
        self.handler.send_message('news', message, touser, toparty, totag, safe, enable_duplicate_check,
                                  duplicate_check_interval, **kwargs)

    def send_mpnews(self, title, thumb_media_id, author=None, content_source_url=None, content=None, digest=None,
                    touser=None,
                    toparty=None,
                    totag=None,
                    safe=0,
                    enable_duplicate_check=0,
                    duplicate_check_interval=1800, **kwargs):
        """
        发送图文消息（mpnews）
        :param title: 标题，不超过128个字节，超过会自动截断（支持id转译）
        :param thumb_media_id: 图文消息缩略图的media_id, 可以通过素材管理接口获得。此处thumb_media_id即上传接口返回的media_id
        :param author: 图文消息的作者，不超过64个字节
        :param content_source_url: 图文消息点击“阅读原文”之后的页面链接
        :param content: 图文消息的内容，支持html标签，不超过666 K个字节（支持id转译）
        :param digest: 图文消息的描述，不超过512个字节，超过会自动截断（支持id转译）
        :param touser: 指定接收消息的成员，成员ID列表（多个接收者用‘|’分隔，最多支持1000个）。特殊情况：指定为"@all"，则向该企业应用的全部成员发送
        :param toparty: 指定接收消息的部门，部门ID列表，多个接收者用‘|’分隔，最多支持100个。当touser为"@all"时忽略本参数
        :param totag: 指定接收消息的标签，标签ID列表，多个接收者用‘|’分隔，最多支持100个。当touser为"@all"时忽略本参数
        :param safe: 表示是否是保密消息，0表示可对外分享，1表示不能分享且内容显示水印，默认为0
        :param enable_duplicate_check: 表示是否开启重复消息检查，0表示否，1表示是，默认0
        :param duplicate_check_interval: 表示是否重复消息检查的时间间隔，默认1800s，最大不超过4小时
        :param kwargs: 其它参数
        :return:
        """
        message = {
            'articles': [{
                'title': title,
                'thumb_media_id': thumb_media_id,
                'content_source_url': content_source_url,
                'author': author,
                'content': content,
                'digest': digest,
            }]
        }
        self.handler.send_message("mpnews", message, touser, toparty, totag, safe, enable_duplicate_check,
                                  duplicate_check_interval, **kwargs)

    def upload_image(self, media_path):
        """
        上传临时素材[图片]，得到 media_id, 该 media_id 三天内有效
        限制：文件大小应在 5B ~ 10MB 之间，支持JPG,PNG格式
        :param media_path: 文件路径
        :return: media_id
        """
        media_id = self.handler.upload_media('image', media_path)
        return media_id

    def upload_voice(self, media_path):
        """
        上传临时素材[语音]，得到 media_id, 该 media_id 三天内有效
        限制：文件大小应在 5B ~ 2MB 之间，播放长度不超过60s，仅支持AMR格式
        :param media_path: 文件路径
        :return: media_id
        """
        media_id = self.handler.upload_media('voice', media_path)
        return media_id

    def upload_video(self, media_path):
        """
        上传临时素材[视频]，得到 media_id, 该 media_id 三天内有效
        限制：文件大小应在 5B ~ 10MB 之间，支持MP4格式
        :param media_path: 文件路径
        :return: media_id
        """
        media_id = self.handler.upload_media('video', media_path)
        return media_id

    def upload_file(self, media_path):
        """
        上传临时素材[普通文件]，得到 media_id, 该 media_id 三天内有效
        限制：文件大小应在 5B ~ 20MB 之间
        :param media_path: 文件路径
        :return: media_id
        """
        media_id = self.handler.upload_media('file', media_path)
        return media_id

    def upload_forever_image(self, image_path):
        """
        上传永久图片，得到图片 url， 该 url 永久有效
        返回的图片URL，仅能用于图文消息正文中的图片展示，或者给客户发送欢迎语等；若用于非企业微信环境下的页面，图片将被屏蔽。
        限制：图片文件大小应在 5B ~ 2MB 之间
        限制：每个企业每月最多可上传3000张图片，每天最多可上传1000张图片
        :param image_path: 图片路径
        :return: 图片 url
        """
        img_url = self.handler.upload_forever_image(image_path)
        return img_url
