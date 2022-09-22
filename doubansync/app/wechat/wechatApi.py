from abc import ABC, abstractmethod


class WeChatApi(ABC):
    """
    接口类，定义所有的接口
    """
    # @abstractmethod
    # def get_token(self, *args, **kwargs):
    #     pass

    @abstractmethod
    def send_text(self, *args, **kwargs):
        pass

    @abstractmethod
    def send_image(self, *args, **kwargs):
        pass

    @abstractmethod
    def send_voice(self, *args, **kwargs):
        pass

    @abstractmethod
    def send_video(self, *args, **kwargs):
        pass

    @abstractmethod
    def send_file(self, *args, **kwargs):
        pass

    @abstractmethod
    def send_textcard(self, *args, **kwargs):
        pass

    @abstractmethod
    def send_news(self, *args, **kwargs):
        pass

    @abstractmethod
    def send_mpnews(self, *args, **kwargs):
        pass

    # @abstractmethod
    # def send_markdown(self, *args, **kwargs):
    #     pass

    @abstractmethod
    def upload_image(self, *args, **kwargs):
        pass

    @abstractmethod
    def upload_voice(self, *args, **kwargs):
        pass

    @abstractmethod
    def upload_video(self, *args, **kwargs):
        pass

    @abstractmethod
    def upload_file(self, *args, **kwargs):
        pass

    # @abstractmethod
    # def get_media(self, *args, **kwargs):
    #     pass

    @abstractmethod
    def upload_p_image(self, *args, **kwargs):
        """
        上传图片得到图片URL，该URL永久有效
        返回的图片URL，仅能用于图文消息正文中的图片展示，或者给客户发送欢迎语等；若用于非企业微信环境下的页面，图片将被屏蔽。
        每个企业每月最多可上传3000张图片，每天最多可上传1000张图片
        """
        pass
