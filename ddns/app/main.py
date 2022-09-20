# -*- coding: UTF-8 -*-
import os
import schedule
import time
import requests
import logging
import logging.config
import yaml
import argparse
from dns.alidns import Alidns
from dns.cloudflare import Cloudflare
from wechat import Wechat

config = {}
with open("logging.yml", 'r') as r:
    config = yaml.safe_load(r)
logging.config.dictConfig(config)
logger = logging.getLogger(__name__)


# 加载配置文件
def load_config(config_path):
    try:
        with open(config_path, 'r') as r:
            config = yaml.safe_load(r)
        return config
    except Exception as e:
        logger.error('加载配置文件失败，请检查配置文件')
        logger.error(e)
        return []


# 获取IP地址，支持v4与v6
def get_public_ip(ip_ver: int, retries: int = 3) -> str:
    ip_addr = None
    ipv4_urls = ["http://whatismyip.akamai.com", "http://4.ipw.cn", "https://v4.ident.me/"]
    ipv6_urls = ["http://6.ipw.cn", "https://v6.ident.me/"]
    if ip_ver == 4:
        for url in ipv4_urls:
            try:
                resp = requests.get(url, timeout=10)
                if resp.status_code != 200:
                    logger.warning(f'从 {url} 获取 IPv{ip_ver} 地址失败: status_code: {resp.status_code}')
                    continue
                ip_addr = resp.content.decode().strip('\n')
                logger.info(f'从 {url} 获取 IPv{ip_ver} 地址成功: {ip_addr}')
                break
            except Exception as e:
                logger.warning(f'从 {url} 获取 IPv{ip_ver} 地址失败: {str(e)}')
                time.sleep(1)
    elif ip_ver == 6:
        for url in ipv6_urls:
            try:
                resp = requests.get(url, timeout=10)
                if resp.status_code != 200:
                    logger.warning(f'从 {url} 获取 IPv{ip_ver} 地址失败: status_code: {resp.status_code}')
                    continue
                ip_addr = resp.content.decode().strip('\n')
                logger.info(f'从 {url} 获取 IPv{ip_ver} 地址成功: {ip_addr}')
                break
            except Exception as e:
                logger.warning(f'从 {url} 获取 IPv{ip_ver} 地址失败: {str(e)}')
                time.sleep(1)
    if not ip_addr and retries > 0:
        ip_addr = get_public_ip(ip_ver, retries - 1)
    if ip_addr:
        return ip_addr
    else:
        logger.error(f"获取 IPv{ip_ver} 地址失败，已尝试3次")
        raise Exception(f"获取 IPv{ip_ver} 地址失败，已尝试3次")


def run_ddns(config) -> None:
    ddns = config.get('ddns')
    message = ""
    if (len(ddns) > 0):
        for v in ddns:
            time.sleep(1)
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
                    if rst['code'] == 0:
                        message += rst['msg'] + "\n"
                except Exception as e:
                    logger.error(f"更新域名({rr}.{domain})的解析记录失败")
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
                    if rst['code'] == 0:
                        message += rst['msg'] + "\n"
                except Exception as e:
                    logger.error(f"更新域名({rr}.{domain})的解析记录失败")
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
        r = r


# 运行
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ddns')
    parser.add_argument('-c', '--config', default="/config/config.yml", help='config file')
    args = parser.parse_args()
    config_path = args.config
    config = load_config(config_path)

    run_ddns(config)
    schedule.every(60).seconds.do(run_ddns, config)  # 每60秒执行一次
    while True:
        schedule.run_pending()
        time.sleep(1)
