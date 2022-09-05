# -*- coding: UTF-8 -*-
import os
import json
import schedule
import time
import requests
import logging
import logging.config
import yaml
from dns.alidns import Alidns
from dns.cloudflare import Cloudflare
from wechat import Wechat

config = {}
with open("logging.yml", 'r') as r:
    config = yaml.safe_load(r)
logging.config.dictConfig(config)
logger = logging.getLogger(__name__)


# 加载配置文件
def load_config():
    try:
        config_file = open("/etc/ddns/config.json", 'r')
        # config_file = open("config_template.json", 'r')
        config_content = config_file.read()
        config_json = json.loads(config_content)
        return config_json
    except Exception as e:
        logger.error('加载配置文件失败，请检查配置文件')
        logger.error(e)
        return []


# 获取IP地址，支持v4与v6
def get_public_ip(ip_ver: int) -> str:
    ip_addr = ""
    ipv4_urls = ["http://whatismyip.akamai.com", "http://4.ipw.cn", "https://v4.ident.me/"]
    ipv6_urls = ["http://6.ipw.cn", "https://v6.ident.me/"]
    if ip_ver == 4:
        for url in ipv4_urls:
            fail_count = 0
            while fail_count < 3:
                try:
                    resp = requests.get(url, timeout=10)
                    ip_addr = resp.content.decode().strip('\n')
                    return ip_addr
                except Exception as e:
                    logger.error(e)
                    fail_count += 1
                    time.sleep(1)
                    pass
    elif ip_ver == 6:
        for url in ipv6_urls:
            fail_count = 0
            while fail_count < 3:
                try:
                    resp = requests.get(url, timeout=10)
                    ip_addr = resp.content.decode().strip('\n')
                    return ip_addr
                except Exception as e:
                    logger.error(e)
                    fail_count += 1
                    time.sleep(1)
                    pass
    raise Exception(f"获取IP版本{ip_ver}地址失败")


def run_ddns() -> None:
    config_json = load_config()
    message = ""
    if (len(config_json) > 0):
        for v in config_json:
            dns = v['dns']
            if dns == 'aliyun':
                id = v['id']
                secret = v['secret']
                domain = v['domain']
                rr = v['rr']
                ttl = v['ttl']
                ip_ver = v['ip_ver']
                try:
                    ip_addr = get_public_ip(ip_ver)
                    alidns = Alidns(id, secret)
                    rst = alidns.ddns(domain, rr, ip_ver, ip_addr, ttl)
                    if rst == 0:
                        message += f"更新域名({rr}.{domain})的解析记录为 {ip_addr} \n"
                except Exception as e:
                    logger.error(e)
                    message += f"更新域名({rr}.{domain})的解析记录失败 \n"
            elif dns == 'dnspod':
                pass
            elif dns == 'cloudflare':
                token = v['token']
                domain = v['domain']
                rr = v['rr']
                ttl = v['ttl']
                ip_ver = v['ip_ver']
                try:
                    ip_addr = get_public_ip(ip_ver)
                    cf = Cloudflare(token)
                    rst = cf.ddns(domain, rr, ip_ver, ip_addr, ttl)
                    if rst == 0:
                        message += f"更新域名({rr}.{domain})的解析记录为 {ip_addr} \n"
                except Exception as e:
                    logger.error(e)
                    message += f"更新域名({rr}.{domain})的解析记录失败 \n"

    # 发送消息
    if message:
        corp_id = os.environ.get('CORP_ID')  # corpid是企业号的标识
        wechat_secret = os.environ.get('SECRET')  # secret是应用凭证密钥
        agent_id = os.environ.get('AGENT_ID')  # agentid 是应用的标识
        wechat = Wechat(corp_id, wechat_secret, agent_id)
        to = '@all'
        subject = 'DDNS更新消息：'
        r = wechat.send_message(to, subject, message, agent_id)



# 运行
if __name__ == '__main__':
    run_ddns()
    schedule.every(60).seconds.do(run_ddns)  # 每60秒执行一次
    while True:
        schedule.run_pending()
        time.sleep(1)
