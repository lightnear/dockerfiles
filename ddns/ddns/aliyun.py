# -*- coding: utf-8 -*-
# update aliyun dns
import sys
import logging

from Tea.core import TeaCore
from alibabacloud_alidns20150109.client import Client as DNSClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_alidns20150109 import models as dns_models

logger = logging.getLogger(__name__)


class Aliyun:
    def __init__(self, access_key_id, access_key_secret):
        config = open_api_models.Config()
        # 传AccessKey ID入config
        config.access_key_id = access_key_id
        # 传AccessKey Secret入config
        config.access_key_secret = access_key_secret
        config.region_id = 'cn-hangzhou'
        self.client = DNSClient(config)

    # 查询域名解析记录
    def describe_domain_records(
        self,
        domain_name: str,
        rr: str,
        record_type: str,
    ) -> list:
        req = dns_models.DescribeDomainRecordsRequest()
        # 主域名
        req.domain_name = domain_name
        # 搜索模式
        req.search_mode = 'ADVANCED'
        # 主机记录
        req.rrkey_word = rr
        # 解析记录类型
        req.type = record_type
        # 解析记录状态
        req.status = 'Enable'
        rst = []
        # logger.info(f'查询域名({rr}.{domain_name})的解析记录(json)↓')
        try:
            resp = self.client.describe_domain_records(req)
            # logger.info(UtilClient.to_jsonstring(TeaCore.to_map(resp)))
            for r in resp.body.domain_records.record:
                if r.rr == rr:
                    rst.append(r)
            return rst
        except Exception as error:
            logger.error(error.message)
            raise

    # 查询域名解析记录
    async def describe_domain_records_async(
        self,
        domain_name: str,
        rr: str,
        record_type: str,
    ) -> list:
        req = dns_models.DescribeDomainRecordsRequest()
        # 主域名
        req.domain_name = domain_name
        # 搜索模式
        req.search_mode = 'ADVANCED'
        # 主机记录
        req.rrkey_word = rr
        # 解析记录类型
        req.type = record_type
        # 解析记录状态
        req.status = 'ENABLE'
        rst = []
        # logger.info(f'查询域名({rr}.{domain_name})的解析记录(json)↓')
        try:
            resp = await self.client.describe_domain_records_async(req)
            # logger.info(UtilClient.to_jsonstring(TeaCore.to_map(resp)))
            for r in resp.body.domain_records:
                if r.RR == rr:
                    rst.append(r)
            return rst
        except Exception as error:
            logger.error(error.message)
            raise

    # 添加域名解析记录
    def add_domain_record(
        self,
        domain_name: str,
        rr: str,
        record_type: str,
        value: str,
        ttl: int,
    ) -> str:
        req = dns_models.AddDomainRecordRequest()
        req.domain_name = domain_name
        req.rr = rr
        req.type = record_type
        req.value = value
        req.ttl = ttl
        # logger.info('添加域名解析记录的结果(json)↓')
        try:
            resp = self.client.add_domain_record(req)
            # logger.info(UtilClient.to_jsonstring(TeaCore.to_map(resp)))
            return resp.body.record_id
        except Exception as error:
            logger.error(error.message)
            raise

    # 添加域名解析记录
    async def add_domain_record_async(
        self,
        domain_name: str,
        rr: str,
        record_type: str,
        value: str,
        ttl: int,
    ) -> str:
        req = dns_models.AddDomainRecordRequest()
        req.domain_name = domain_name
        req.rr = rr
        req.type = record_type
        req.value = value
        req.ttl = ttl
        # logger.info('添加域名解析记录的结果(json)↓')
        try:
            resp = await self.client.add_domain_record_async(req)
            # logger.info(UtilClient.to_jsonstring(TeaCore.to_map(resp)))
            return resp.body.record_id
        except Exception as error:
            logger.error(error.message)
            raise

    # 更新域名解析记录
    def update_domain_record(
        self,
        record_id: str,
        rr: str,
        record_type: str,
        value: str,
        ttl: int,
    ) -> str:
        req = dns_models.UpdateDomainRecordRequest()
        req.record_id = record_id
        req.rr = rr
        req.type = record_type
        req.value = value
        req.ttl = ttl
        # logger.info('更新域名解析记录的结果(json)↓')
        try:
            resp = self.client.update_domain_record(req)
            # logger.info(UtilClient.to_jsonstring(TeaCore.to_map(resp)))
            return resp.body.record_id
        except Exception as error:
            logger.error(error.message)
            raise

    # 更新域名解析记录
    async def update_domain_record_async(
        self,
        record_id: str,
        rr: str,
        record_type: str,
        value: str,
        ttl: int,
    ) -> str:
        req = dns_models.UpdateDomainRecordRequest()
        req.record_id = record_id
        req.rr = rr
        req.type = record_type
        req.value = value
        req.ttl = ttl
        # logger.info('更新域名解析记录的结果(json)↓')
        try:
            resp = await self.client.update_domain_record_async(req)
            # logger.info(UtilClient.to_jsonstring(TeaCore.to_map(resp)))
            return resp.body.record_id
        except Exception as error:
            logger.error(error.message)
            raise

    # 删除域名解析记录
    def delete_domain_record(
        self,
        record_id: str,
    ) -> str:
        req = dns_models.DeleteDomainRecordRequest()
        req.record_id = record_id
        # logger.info('删除域名解析记录的结果(json)↓')
        try:
            resp = self.client.delete_domain_record(req)
            # logger.info(UtilClient.to_jsonstring(TeaCore.to_map(resp)))
            return resp.body.record_id
        except Exception as error:
            logger.error(error.message)
            raise

    # 删除域名解析记录
    async def delete_domain_record_async(
        self,
        record_id: str,
    ) -> str:
        req = dns_models.DeleteDomainRecordRequest()
        req.record_id = record_id
        # logger.info('删除域名解析记录的结果(json)↓')
        try:
            resp = await self.client.delete_domain_record_async(req)
            # logger.info(UtilClient.to_jsonstring(TeaCore.to_map(resp)))
            return resp.body.record_id
        except Exception as error:
            logger.error(error.message)
            raise

    # 更新DNS记录
    # 0：更新成功
    # 1：与现在DNS相同
    def ddns(
        self,
        domain_name: str,
        rr: str,
        ip_ver: int,
        ip_addr: str,
        ttl: int,
    ) -> int:
        record_type = 'A'
        if ip_ver == 6:
            record_type = 'AAAA'
        # 1.查询域名解析记录
        rst = self.describe_domain_records(domain_name, rr, record_type)
        if len(rst) == 0:
            self.add_domain_record(domain_name, rr, record_type, ip_addr, ttl)
            logger.info(f'添加域名({rr}.{domain_name})的解析记录为 {ip_addr}')
            return 0
        elif len(rst) == 1:
            if rst[0].value == ip_addr:
                logger.info(f'域名({rr}.{domain_name})的解析记录为 {ip_addr}, 保持不变')
                return 1
            else:
                self.update_domain_record(rst[0].record_id, rr, record_type, ip_addr, ttl)
                logger.info(f'更新域名({rr}.{domain_name})的解析记录为 {ip_addr}')
                return 0
        else:
            for r in rst:
                self.delete_domain_record(r.record_id)
            self.add_domain_record(domain_name, rr, record_type, ip_addr, ttl)
            logger.info(f'更新域名({rr}.{domain_name})的解析记录为 {ip_addr}')
            return 0


