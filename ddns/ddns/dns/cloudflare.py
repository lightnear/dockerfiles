# -*- coding: utf-8 -*-
"""
CloudFlare API
CloudFlare 接口解析操作库
https://api.cloudflare.com/#dns-records-for-a-zone-properties
"""

import json
import logging
from http.client import HTTPSConnection
from urllib.parse import urlencode

# logger = logging.getLogger(__name__)


class Cloudflare:

    def __init__(self, cf_token) -> None:
        self.logger = logging.getLogger(__name__)
        self.cf_token = cf_token
        # API endpoint
        self.endpoint = 'api.cloudflare.com'

    def request(self, method, action, param=None, **params):
        """
        发送请求数据
        """
        if param:
            params.update(param)

        params = dict((k, params[k]) for k in params if params[k] is not None)

        conn = HTTPSConnection(self.endpoint)

        if method in ['PUT', 'POST', 'PATCH']:
            # 从public_v(4,6)获取的IP是bytes类型，在json.dumps时会报TypeError
            params['content'] = str(params.get('content'))
            params = json.dumps(params)
        else:  # (GET, DELETE) where DELETE doesn't require params in Cloudflare
            if params:
                action += '?' + urlencode(params)
            params = None

        headers = {"Content-type": "application/json", "Authorization": "Bearer " + self.cf_token}
        self.logger.debug(f'url: {self.endpoint}/client/v4/{action}, params: {params}, headers: {headers}')
        conn.request(method, '/client/v4/' + action, params, headers)
        response = conn.getresponse()
        res = response.read().decode('utf8')
        conn.close()
        if response.status < 200 or response.status >= 300:
            self.logger.warning('%s : error[%d]:%s', action, response.status, res)
            raise Exception(res)
        else:
            data = json.loads(res)
            if not data:
                raise Exception("Empty Response")
            elif data.get('success'):
                return data.get('result', [{}])
            else:
                raise Exception(data.get('errors', [{}]))

    def get_zone_id(self, domain):
        """
        获取主域名ID(Zone_ID)
        https://api.cloudflare.com/#zone-list-zones
        """
        zone_id = None
        zones = self.request('GET', 'zones', name=domain)
        zone_id = zones[0].get('id')
        return zone_id

    def get_records(self, zone_id, domain, rr, record_type):
        """
        获取记录ID
        返回满足条件的所有记录[]
        TODO 大于100翻页
        https://api.cloudflare.com/#dns-records-for-a-zone-list-dns-records
        """
        action = 'zones/' + zone_id + '/dns_records'
        params = {'name': rr + '.' + domain, 'per_page': 500, 'type': record_type}
        records = self.request('GET', action, params)
        return records

    def add_record(self, zone_id, domain, rr, record_type, content, ttl):
        """
        添加记录
        add
        https://api.cloudflare.com/#dns-records-for-a-zone-create-dns-record
        """
        action = 'zones/' + zone_id + '/dns_records'
        params = {'name': rr + '.' + domain, 'type': record_type, 'content': content, 'ttl': ttl}
        data = self.request('POST', action, params)
        record_id = ''
        if data:
            record_id = data.get('id')
        return record_id

    def update_record(self, zone_id, record_id, domain, rr, record_type, content, ttl):
        """
        更新记录
        update
        https://api.cloudflare.com/#dns-records-for-a-zone-update-dns-record
        """
        action = 'zones/' + zone_id + '/dns_records/' + record_id
        params = {'name': rr + '.' + domain, 'type': record_type, 'content': content, 'ttl': ttl}
        data = self.request('PUT', action, params)
        record_id = ''
        if data:
            record_id = data.get('id')
        return record_id

    def delete_record(self, zone_id, record_id):
        """
        更新记录
        update
        https://api.cloudflare.com/#dns-records-for-a-zone-update-dns-record
        """
        action = 'zones/' + zone_id + '/dns_records/' + record_id
        params = {}
        data = self.request('DELETE', action, params)
        record_id = ''
        if data:
            record_id = data.get('id')
        return record_id

    def ddns(self, domain, rr, ip_ver, ip_addr, ttl):
        record_type = 'A'
        if ip_ver == 6:
            record_type = 'AAAA'
        # 0. 获取 zone id
        zone_id = self.get_zone_id(domain)
        # 1.查询域名解析记录
        records = self.get_records(zone_id, domain, rr, record_type)
        # 2.1 查询不到则新增
        if len(records) == 0:
            self.add_record(zone_id, domain, rr, record_type, ip_addr, ttl)
            self.logger.info(f'添加域名({rr}.{domain})的解析记录为 {ip_addr}')
            return 0
        # 2.2 只查到一条
        elif len(records) == 1:
            if records[0].get('content') == ip_addr:
                self.logger.info(f'域名({rr}.{domain})的解析记录为 {ip_addr}, 保持不变')
                return 1
            else:
                record_id = records[0].get('id')
                self.update_record(zone_id, record_id, domain, rr, record_type, ip_addr, ttl)
                self.logger.info(f'更新域名({rr}.{domain})的解析记录为 {ip_addr}')
                return 0
        else:
            for record in records:
                self.delete_record(zone_id, record.get('id'))
            self.add_record(zone_id, domain, rr, record_type, ip_addr, ttl)
            self.logger.info(f'更新域名({rr}.{domain})的解析记录为 {ip_addr}')
            return 0


