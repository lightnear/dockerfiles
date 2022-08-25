# -*- coding: utf-8 -*-
"""
AliDNS API
阿里DNS解析操作库
https://help.aliyun.com/document_detail/29739.html
"""

from hashlib import sha1
from hmac import new as hmac
from uuid import uuid4
from base64 import b64encode
import json
from datetime import datetime
import logging
from http.client import HTTPSConnection
from urllib.parse import urlencode, quote_plus, quote

# logger = logging.getLogger(__name__)


class Alidns:
    def __init__(self, access_key_id, access_key_secret):
        self.logger = logging.getLogger(__name__)
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        # API endpoint
        self.site = "alidns.aliyuncs.com"
        self.method = 'POST'

    def signature(self, params):
        """
        计算签名,返回签名后的查询参数
        """
        params.update({
            'Format': 'json',
            'Version': '2015-01-09',
            'AccessKeyId': self.access_key_id,
            'Timestamp': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            'SignatureMethod': 'HMAC-SHA1',
            'SignatureNonce': uuid4(),
            'SignatureVersion': "1.0",
        })
        query = urlencode(sorted(params.items()))
        query = query.replace('+', '%20')
        self.logger.debug(f'query: {query}')
        sign = self.method + "&" + quote_plus("/") + "&" + quote(query, safe='')
        self.logger.debug(f'signString: {sign}')

        sign = hmac((self.access_key_secret + "&").encode('utf-8'), sign.encode('utf-8'), sha1).digest()
        sign = b64encode(sign).strip()
        params["Signature"] = sign
        return params

    def request(self, param=None, **params):
        """
        发送请求数据
        """
        if param:
            params.update(param)
        params = dict((k, params[k]) for k in params if params[k] is not None)
        params = self.signature(params)
        self.logger.debug(f'params: {params}')

        conn = HTTPSConnection(self.site)
        conn.request(self.method, '/', urlencode(params), {"Content-type": "application/x-www-form-urlencoded"})
        response = conn.getresponse()
        data = response.read().decode('utf8')
        conn.close()

        if response.status < 200 or response.status >= 300:
            self.logger.warning('%s : error[%d]: %s', params['Action'], response.status, data)
            raise Exception(data)
        else:
            data = json.loads(data)
            return data

    def get_records(self, domain, rr, record_type):
        """
        获取记录ID
        返回满足条件的所有记录[]
        https://help.aliyun.com/document_detail/29776.html
        TODO 大于500翻页
        """
        records = []
        params = {
            'Action': 'DescribeDomainRecords',
            'DomainName': domain,
            'KeyWord': rr,
            'SearchMode': 'EXACT',
            'PageSize': 500
        }
        data = self.request(params)
        if data:
            for record in data.get('DomainRecords').get('Record'):
                if record.get('Type') == record_type:
                    records.append(record)
        return records

    def add_record(self, domain, rr, record_type, value, ttl):
        """
        添加记录
        add
        https://help.aliyun.com/document_detail/29772.html
        """
        params = {
            'Action': 'AddDomainRecord',
            'DomainName': domain,
            'RR': rr,
            'Type': record_type,
            'Value': value,
            'TTL': ttl
        }
        record_id = ''
        data = self.request(params)
        if data:
            record_id = data.get('RecordId')
        return record_id

    def update_record(self, record_id, rr, record_type, value, ttl):
        """
        更新记录
        update
        https://help.aliyun.com/document_detail/29774.html
        """
        params = {
            'Action': 'UpdateDomainRecord',
            'RecordId': record_id,
            'RR': rr,
            'Type': record_type,
            'Value': value,
            'TTL': ttl
        }
        record_id = ''
        data = self.request(params)
        if data:
            record_id = data.get('RecordId')
        return record_id

    def delete_record(self, record_id):
        """
        删除记录
        delete
        https://help.aliyun.com/document_detail/29773.html
        """
        params = {
            'Action': 'DeleteDomainRecord',
            'RecordId': record_id
        }
        record_id = ''
        data = self.request(params)
        if data:
            record_id = data.get('RecordId')
        return record_id

    def ddns(self, domain, rr, ip_ver, ip_addr, ttl):
        record_type = 'A'
        if ip_ver == 6:
            record_type = 'AAAA'
        # 1.查询域名解析记录
        records = self.get_records(domain, rr, record_type)
        # 2.1 查询不到则新增
        if len(records) == 0:
            self.add_record(domain, rr, record_type, ip_addr, ttl)
            self.logger.info(f'添加域名({rr}.{domain})的解析记录为 {ip_addr}')
            return 0
        # 2.2 只查到一条
        elif len(records) == 1:
            if records[0].get('Value') == ip_addr:
                self.logger.info(f'域名({rr}.{domain})的解析记录为 {ip_addr}, 保持不变')
                return 1
            else:
                record_id = records[0].get('RecordId')
                self.update_record(record_id, rr, record_type, ip_addr, ttl)
                self.logger.info(f'更新域名({rr}.{domain})的解析记录为 {ip_addr}')
                return 0
        else:
            for record in records:
                self.delete_record(record.get('RecordId'))
            self.add_record(domain, rr, record_type, ip_addr, ttl)
            self.logger.info(f'更新域名({rr}.{domain})的解析记录为 {ip_addr}')
            return 0

