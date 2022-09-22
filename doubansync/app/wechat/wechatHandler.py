import json
import logging
import os
import platform
import tempfile
import time
import requests
import yaml
from pathlib import Path


class WechatHandler(object):
    def __init__(self, corpid, corpsecret, agentid, base_url=None) -> None:
        self.logger = logging.getLogger(__name__)
        self.corpid = corpid
        self.corpsecret = corpsecret
        self.agentid = agentid
        self.base_url = 'https://qyapi.weixin.qq.com/cgi-bin'
        if base_url:
            self.base_url = base_url

    @staticmethod
    def is_image(file):
        if not (file.suffix in (".JPG", ".PNG", ".jpg", ".png") and (5 <= file.stat().st_size <= 10 * 1024 * 1024)):
            raise TypeError(
                {"Code": "ERROR", "message": '图片文件不合法, 请检查文件类型(jpg, png, JPG, PNG)或文件大小(5B~10M)'})

    @staticmethod
    def is_voice(file):
        if not (file.suffix in (".AMR", ".amr") and (5 <= file.stat().st_size <= 2 * 1024 * 1024)):
            raise TypeError({"Code": "ERROR", "message": '语音文件不合法, 请检查文件类型(AMR, amr)或文件大小(5B~2M)'})

    @staticmethod
    def is_video(file):
        if not (file.suffix in (".MP4", ".mp4") and (5 <= file.stat().st_size <= 10 * 1024 * 1024)):
            raise TypeError({"Code": "ERROR", "message": '视频文件不合法, 请检查文件类型(MP4, mp4)或文件大小(5B~10M)'})

    @staticmethod
    def is_file(file):
        if not (file.is_file() and (5 <= file.stat().st_size <= 20 * 1024 * 1024)):
            raise TypeError({"Code": "ERROR", "message": '普通文件不合法, 请检查文件类型或文件大小(5B~20M)'})

    @staticmethod
    def is_forever_image(file):
        if not (file.suffix in (".JPG", ".PNG", ".jpg", ".png") and (5 <= file.stat().st_size <= 2 * 1024 * 1024)):
            raise TypeError(
                {"Code": "ERROR", "message": '图片文件不合法, 请检查文件类型(jpg, png, JPG, PNG)或文件大小(5B~2M)'})

    def media_check(self, media_type, media_path):
        """
        验证上传文件是否符合标准
        :param file_type: 文件类型(image,voice,video,file)
        :param path:
        :return:
        """
        p = Path(media_path)
        media_types = {
            "image": self.is_image,
            "voice": self.is_voice,
            "video": self.is_video,
            "file": self.is_file,
            "forever_image": self.is_forever_image
        }
        chat_type = media_types.get(media_type, None)
        if not chat_type:
            raise TypeError({"errcode": 'ERROR', "errmsg": '不支持的文件类型，请检查文件类型(image,voice,video,file)'})
        chat_type(p)
        return {"media": (p.name, p.read_bytes())}

    def _get(self, url, hearders=None, params=None):
        url = f'{self.base_url}{url}'
        if not hearders:
            hearders = {'content-type': 'application/json; charset=utf-8'}
        try:
            rsp = requests.get(url, headers=hearders, params=params)
            rsp.raise_for_status()
            result = rsp.json()
            if result.get('errcode') == 0:
                return result
            elif result.get('errcode') == 40013 or result.get('errcode') == 40001:
                raise ValueError({'errcode': result.get("errcode"), 'errmsg': 'corpid 或 corpsecret 错误，请检查'})
            else:
                raise ValueError({'errcode': result.get("errcode"), 'errmsg': result.get('errmsg')})
        except Exception as e:
            raise e

    def _post(self, url, hearders=None, params=None, data=None, files=None):
        url = f'{self.base_url}{url}'
        if not hearders:
            hearders = {'content-type': 'application/json; charset=utf-8'}
        try:
            rsp = requests.post(url, headers=hearders, params=params, data=data, files=files)
            self.logger.debug(f'{rsp.status_code}, {rsp.text}')
            rsp.raise_for_status()
            result = rsp.json()
            if result.get('errcode') == 0:
                return result
            else:
                raise ValueError({'errcode': result.get("errcode"), 'errmsg': result.get('errmsg')})
        except Exception as e:
            raise e

    def get_token(self):
        tempdir = '/tmp' if platform.system() == 'Darwin' else tempfile.gettempdir()
        token_file = os.path.join(tempdir, '.wechat_token.yml')
        # 先尝试从文件获取 token
        if os.path.isfile(token_file):
            try:
                with open(token_file, 'r', encoding='utf-8') as r:
                    config = yaml.safe_load(r)
                if int(config.get('expire')) > int(time.time()) + 600:
                    return config.get('access_token')
            except Exception as e:
                self.logger.warning(f'读取配置文件失败, 重新获取：{str(e)}')

        return self._get_token()

    def _get_token(self):
        url = '/gettoken'
        params = {"corpid": self.corpid, "corpsecret": self.corpsecret}
        token = None
        try:
            rsp = self._get(url, params=params)
            self.logger.debug(rsp)
            token = {'access_token': rsp.get('access_token'), 'expire': int(time.time()) + int(rsp.get('expires_in'))}
        except Exception as e:
            self.logger.error(f'获取token失败: {str(e)}')

        tempdir = '/tmp' if platform.system() == 'Darwin' else tempfile.gettempdir()
        token_file = os.path.join(tempdir, '.wechat_token.yml')
        try:
            with open(token_file, 'w', encoding='utf-8') as f:
                f.write(yaml.dump(token))
                self.logger.info('token 持久化成功')
        except Exception as e:
            self.logger.warning(f'token 持久化失败: {str(e)}')
        return token.get('access_token')

    def send_message(self, message_type, message, touser=None, toparty=None, totag=None, safe=0,
                     enable_duplicate_check=0, duplicate_check_interval=1800, **kwargs):
        """
        发送消息的主要接口封装和发起请求
        :param message_type: 发送消息的类型
        :param message: 消息内容
        :param touser: 指定接收消息的成员，成员ID列表（多个接收者用‘|’分隔，最多支持1000个）。特殊情况：指定为"@all"，则向该企业应用的全部成员发送
        :param toparty: 指定接收消息的部门，部门ID列表，多个接收者用‘|’分隔，最多支持100个。当touser为"@all"时忽略本参数
        :param totag: 指定接收消息的标签，标签ID列表，多个接收者用‘|’分隔，最多支持100个。当touser为"@all"时忽略本参数
        :param safe: 表示是否是保密消息，0表示可对外分享，1表示不能分享且内容显示水印，默认为0
        :param enable_duplicate_check: 表示是否开启重复消息检查，0表示否，1表示是，默认0
        :param duplicate_check_interval: 表示是否重复消息检查的时间间隔，默认1800s，最大不超过4小时
        :param kwargs: 其它参数
        :return:
        """
        url = '/message/send'
        params = {'access_token': self.get_token()}
        data = {'msgtype': message_type, 'agentid': self.agentid, message_type: message, 'safe': safe,
                'enable_duplicate_check': enable_duplicate_check,
                'duplicate_check_interval': duplicate_check_interval
                }

        if not (touser or toparty or totag):
            data["touser"] = "@all"
        else:
            if touser:
                data["touser"] = touser
            if toparty:
                data["toparty"] = toparty
            if totag:
                data["totag"] = totag

        # 判断是否需要上传
        if message_type in ('image', 'voice', 'video', 'file'):
            media_path = message.get('media_path')
            media_id = self.upload_media(message_type, media_path)
            if not media_id:
                return None
            message["media_id"] = media_id

        try:
            self.logger.info(params)
            self.logger.info(data)
            rsp = self._post(url, params=params, data=json.dumps(data))
            self.logger.error(f'发送 {message_type} 消息成功：{message}')
            return rsp
        except Exception as e:
            self.logger.error(f'发送 {message_type} 消息失败：{message}')
            self.logger.error(e)
            return None

    def upload_media(self, media_type, media_path):
        """
        上传临时素材，得到 media_id, 该 media_id 三天内有效
        :param media_type: 文件类型
        :param media_path: 文件路径
        :return: media_id
        """
        url = '/media/upload'
        hearders = {'content-type': 'multipart/form-data'}
        params = {'access_token': self.get_token(), 'type': media_type}
        try:
            files = self.media_check(media_type, media_path)
            rsp = self._post(url, hearders=hearders, params=params, files=files)
            media_id = rsp.get('media_id')
            self.logger.info(f'上传临时素材成功: {media_type} {media_path} -> {media_id}')
            return media_id
        except Exception as e:
            self.logger.error(f'上传临时素材失败：{media_type} {media_path}')
            self.logger.error(e)
            return None

    def upload_forever_image(self, image_path):
        """
        上传永久图片，得到图片 url， 该 url 永久有效
        返回的图片URL，仅能用于图文消息正文中的图片展示，或者给客户发送欢迎语等；若用于非企业微信环境下的页面，图片将被屏蔽。
        每个企业每月最多可上传3000张图片，每天最多可上传1000张图片
        :param image_path: 图片路径
        :return: 图片 url
        """
        url = '/media/uploadimg'
        hearders = {'content-type': 'multipart/form-data'}
        params = {'access_token': self.get_token()}
        try:
            files = self.media_check('forever_image', image_path)
            rsp = self._post(url, hearders=hearders, params=params, files=files)
            img_url = rsp.get('url')
            self.logger.info(f'上传永久图片成功: {image_path} -> {img_url}')
            return img_url
        except Exception as e:
            self.logger.error(f'上传永久图片失败：{image_path}')
            self.logger.error(e)
            return None
