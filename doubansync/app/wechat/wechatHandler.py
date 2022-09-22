import os
import platform
import tempfile
import logging
import yaml
import time
import requests
import json
from pathlib import Path


class WechatHandler(object):

    def __init__(self, corpid, corpsecret, agentid, base_url=None) -> None:
        self.logger = logging.getLogger(__name__)
        self.corpid = corpid
        self.corpsecret = corpsecret
        self.agentid = agentid
        self.base_url = 'https://qyapi.weixin.qq.com/cgi-bin'
        if not base_url:
            self.base_url = base_url

    @staticmethod
    def is_image(file):
        if not (file.suffix in (".JPG", ".PNG", ".jpg", ".png") and (5 <= file.stat().st_size <= 10 * 1024 * 1024)):
            raise TypeError({"Code": "ERROR", "message": '图片文件不合法, 请检查文件类型(jpg, png, JPG, PNG)或文件大小(5B~10M)'})

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
    def is_p_image(file):
        if not (file.suffix in (".JPG", ".PNG", ".jpg", ".png") and (5 <= file.stat().st_size <= 2 * 1024 * 1024)):
            raise TypeError({"Code": "ERROR", "message": '图片文件不合法, 请检查文件类型(jpg, png, JPG, PNG)或文件大小(5B~2M)'})

    def file_check(self, file_type, file_path):
        """
        验证上传文件是否符合标准
        :param file_type: 文件类型(image,voice,video,file)
        :param path:
        :return:
        """
        p = Path(file_path)
        filetypes = {
            "image": self.is_image,
            "voice": self.is_voice,
            "video": self.is_video,
            "file": self.is_file,
            "p_image": self.is_p_image
        }
        chat_type = filetypes.get(file_type, None)
        if not chat_type:
            raise TypeError({"Code": 'ERROR', "message": '不支持的文件类型，请检查文件类型(image,voice,video,file)'})
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
                raise ValueError({'Code': result.get("errcode"), 'message': 'corpid 或 corpsecret 错误，请检查'})
            else:
                raise ValueError({'Code': result.get("errcode"), 'message': result.get('errmsg')})
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
                self.logger.error(f"微信请求失败：{rsp.get('errcode')} {rsp.get('errmsg')}")
                raise ValueError({'Code': result.get("errcode"), 'message': result.get('errmsg')})
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

    def send_message(self, message_type, message, touser=None, todept=None, totags=None):
        """
        发送消息的主要接口封装和发起请求
        :param message_type: 发送消息的类型
        :param message: 发送消息的内容
        :param touser: 发送到具体的用户，当此参数为@all时，忽略todept,totags 参数并发送到全部人，此参数默认为@all
        用户名用 | 拼接。最多支持100个
        :param todept: 发送到部门，当tousers为默认@all 此参数会被忽略.部门之间用 | 拼接。最多支持100个
        :param totags: 发送到标签的用用户,当tousers为默认@all 此参数会被忽略. 标签之间用 | 拼接.最多支持100个
        :return:
        """
        url = '/message/send'
        params = {'access_token': self.get_token()}
        data = {'msgtype': message_type, 'agentid': self.agentid, message_type: message}

        if not (touser or todept or totags):
            data["touser"] = "@all"
        else:
            if touser:
                data["touser"] = touser
            if todept:
                data["toparty"] = todept
            if totags:
                data["totag"] = totags

        # 判断是否需要上传
        if message_type in ("image", "voice", "video", "file"):
            filepath = message.get("media_id")
            media_id = self.upload_media(message_type, filepath)
            message["media_id"] = media_id
        self.logger.info(params)
        self.logger.info(data)
        self._post(url, params=params, data=json.dumps(data))
        self.logger.info(f"发送 {message_type} 消息成功...")

    def upload_media(self, file_type, file_path):
        """
        上传临时素材， 3天有效期
        :param file_type: 文件类型
        :param path: 文件路径
        :return: media_id
        """
        url = '/media/upload'
        hearders = {'content-type': 'multipart/form-data'}
        params = {'access_token': self.get_token(), 'type': file_type}
        files = self.file_check(file_type, file_path)
        rsp = self._post(url, hearders=hearders, params=params, files=files)
        self.logger.info(f'临时素材上传成功: {file_type} {file_path}')
        return rsp.get('media_id')

    def upload_image(self, image_path):
        """
        上传临时素材， 3天有效期
        :param file_type: 文件类型
        :param path: 文件路径
        :return: media_id
        """
        url = '/media/uploadimg'
        hearders = {'content-type': 'multipart/form-data'}
        params = {'access_token': self.get_token()}
        files = self.file_check('p_image', image_path)
        rsp = self._post(url, hearders=hearders, params=params, files=files)
        self.logger.info(rsp)
        self.logger.info(f'图片上传成功: {image_path}')
        return rsp.get('url')
