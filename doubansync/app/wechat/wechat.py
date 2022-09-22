import os
import logging
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
                self.logger.warning(f'读取配置文件失败, 重新获取：{str(e)}')
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
                  
        text_msg = {"content": content}
        self.handler.send_message("text", text_msg, **kwargs)

    def send_image(self, image_path, **kwargs):
        """
        发送图片消息，仅支持jpg,png格式，大小5B~2M
        :param image_path: 发送图片的本地路径
        :param kwargs: 可选择发送对象，tousers(用户), todept(部门), totags(标签用户).
        """
        image_msg = {"media_id": image_path}
        self.handler.send_message("image", image_msg, **kwargs)

    def send_voice(self, voice_path, **kwargs):
        """
        发送语音消息，仅支持amr格式，大小5B~2M
        :param voice_path: 发送语音文件的本地路径
        :param kwargs: 可选择发送对象，tousers(用户), todept(部门), totags(标签用户).
        :return:
        """
        voice_msg = {"media_id": voice_path}
        self.handler.send_message("voice", voice_msg, **kwargs)

    def send_video(self, video_path, title=None, desc=None, **kwargs):
        """
        发送视频消息，仅支持MP4格式的视频消息，大小5B~10M
        :param video_path: 发送视频文件的本地路径
        :param title: 视频消息的标题，不超过128个字节，超过会自动截断.当不指定时默认为上传视频的文件名
        :param desc: 视频消息的描述，不超过512个字节，超过会自动截断
        :param kwargs: 可选择发送对象，tousers(用户), todept(部门), totags(标签用户).
        :return:
        """
        video_msg = {"media_id": video_path}

        if title:
            video_msg["title"] = title

        if desc:
            video_msg["description"] = desc

        self.handler.send_message("video", video_msg, **kwargs)

    def send_file(self, file_path, **kwargs):
        """
        发送文件消息, 大小5B~10M
        :param file_path: 发送文件的本地路径
        :param kwargs: tousers(用户), todept(部门), totags(标签用户).
        :return:
        """
        file_msg = {"media_id": file_path}
        self.handler.send_message("file", file_msg, **kwargs)

    def send_textcard(self, title, desc, link, btn="详情", **kwargs):
        """
        发送文本卡片消息
        :param card_title: 标题，不超过128个字节，超过会自动截断
        :param desc: 描述，不超过512个字节，超过会自动截断
        :param link: 点击后跳转的链接。最长2048字节，请确保包含了协议头(http/https)
        :param btn: 按钮文字。 默认为“详情”， 不超过4个文字，超过自动截断。
        :param kwargs: tousers(用户), todept(部门), totags(标签用户).
        :return:
        """
        textcard_msg = {"title": title, "description": desc, "url": link, "btntxt": btn}
        self.handler.send_message("textcard", textcard_msg, **kwargs)

    def send_news(self, title, desc, link, image_link, **kwargs):
        """
        发送图文卡片消息
        :param card_title: 卡片标题
        :param desc:  卡片描述
        :param link:  点击后跳转的链接
        :param image_link: 图片url
        :param kwargs: tousers(用户), todept(部门), totags(标签用户).
        :return:
        """
        news = {"articles": [{"title": title, "description": desc, "url": link, "picurl": image_link}]}
        self.handler.send_message("news", news, **kwargs)

    def send_mpnews(self, title, digest, media_id, content, **kwargs):
        """
        发送图文卡片消息
        :param card_title: 卡片标题
        :param desc:  卡片描述
        :param link:  点击后跳转的链接
        :param image_link: 图片url
        :param kwargs: tousers(用户), todept(部门), totags(标签用户).
        :return:
        """
        mpnews = {
            "articles": [{
                "title": title,
                "digest": digest,
                "thumb_media_id": media_id,
                'author': 'lightnear',
                "content": content,
                'content_source_url': 'https://dataworld.fun'
            }]
        }
        self.handler.send_message("mpnews", mpnews, **kwargs)

    def upload_image(self, file_path):
        media_id = self.handler.upload_media('image', file_path)
        return media_id

    def upload_voice(self, file_path):
        media_id = self.handler.upload_media('voice', file_path)
        return media_id

    def upload_video(self, file_path):
        media_id = self.handler.upload_media('video', file_path)
        return media_id

    def upload_file(self, file_path):
        media_id = self.handler.upload_media('file', file_path)
        return media_id

    def upload_p_image(self, image_path):
        """
        上传图片，返回图片链接，永久有效，主要用于图文消息卡片. imag_link参数
        图片大小：图片文件大小应在 5B ~ 2MB 之间
        :param image_path:  图片路径
        :return: 图片链接，永久有效
        """
        image_url = self.handler.upload_image(image_path)
        return image_url
