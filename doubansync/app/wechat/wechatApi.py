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
    def upload_forever_image(self, *args, **kwargs):
        pass
