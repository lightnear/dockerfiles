# -*- coding: utf-8 -*-
# send wechat message

import json
import datetime
import requests
import logging


# 根据企业微信api接口文档，定义一个类，使用mpnews类型
# https://qydev.weixin.qq.com/wiki/index.php?title=%E6%B6%88%E6%81%AF%E7%B1%BB%E5%9E%8B%E5%8F%8A%E6%95%B0%E6%8D%AE%E6%A0%BC%E5%BC%8F
# https://developer.work.weixin.qq.com/document/path/90236#%E5%9B%BE%E6%96%87%E6%B6%88%E6%81%AF%EF%BC%88mpnews%EF%BC%89
class Wechat(object):
    logger = None
    to = None
    corp_id = None
    secret = None
    agent_id = None

    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        self.to = '@all'
        self.corp_id = config.get('wechat').get('corpid')
        self.secret = config.get('wechat').get('secret')
        self.agent_id = config.get('wechat').get('agentid')

    # 获取token
    def get_token(self):
        token = ''
        create_time = datetime.datetime.now() - datetime.timedelta(hours=2)
        create_time = create_time.isoformat()
        hour_before = datetime.datetime.now() - datetime.timedelta(hours=1)
        hour_before = hour_before.isoformat()
        # try to get token from file
        try:
            with open('/tmp/wechat_token.json', 'r') as f:
                data = json.load(f)
                token = data['access_token']
                create_time = data['create_time']
        except Exception as e:
            self.logger.error(e)

        if not token or create_time < hour_before:
            url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
            payload = {"corpid": self.corp_id, "corpsecret": self.secret}
            r = requests.get(url=url, params=payload)
            if r.json()['errcode'] == 0:
                data = r.json()
                token = data['access_token']
                data['create_time'] = datetime.datetime.now().isoformat()
                with open('/tmp/wechat_token.json', 'w') as f:
                    f.write(json.dumps(data))
                return token
            else:
                self.logger.error(f"get token fail, {r.json()['errcode']}:{r.json()['errmsg']}")
                return False
        elif token:
            return token
        else:
            return False

    # 发送文本消息
    def send_message(self, subject, message, to=None, agent_id=None):
        if not agent_id:
            agent_id = self.agent_id
        token = self.get_token()
        if token:
            url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % token
            data = {
                "touser": to,  # 企业号中的用户帐号，在zabbix用户Media中配置
                # "totag": tagid,                               # 企业号中的标签id，群发使用（推荐）
                # "toparty": partyid,                           # 企业号中的部门id，群发时使用。
                "msgtype": "text",  # 消息类型。
                "agentid": agent_id,  # 企业号中的应用id。
                "text": {
                    "content": subject + "\n----------\n" + message
                },
                "safe": 0,
                "enable_id_trans": 0,
                "enable_duplicate_check": 0
            }
            payload = json.dumps(data)
            headers = {'Content-Type': 'application/json'}
            r = requests.post(url=url, headers=headers, data=payload)
            if r.json()['errcode'] == 0:
                self.logger.info(f'[wechat] send message to {to} success: {message}')
            else:
                self.logger.error(f'[wechat] send message to {to} fail: {message}')
                self.logger.error(f"[wechat] send message fail: {r.json()['errcode']}:{r.json()['errmsg']}")
            return r.json()
        else:
            self.logger.error("[wechat] send message fail, cannot get token")
