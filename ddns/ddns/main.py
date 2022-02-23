# -*- coding: UTF-8 -*-

import json
from datetime import datetime
import schedule
import time
import requests
from aliyunsdkalidns.request.v20150109 import DescribeDomainRecordsRequest, UpdateDomainRecordRequest, \
    AddDomainRecordRequest
from aliyunsdkcore import client


# 读取配置文件
def get_config_json():
    try:
        config_r = open("/etc/ddns/config.json", 'r')
        config_content = config_r.read()
        config_json = json.loads(config_content)
        return config_json
    except Exception as e:
        print("Load config fail, please recheck config file!")
        print(e)
        return []


# 获取域名信息
# 输出格式：[RecordId, Value]
def get_record_info(ali_ctl, domain, sub_domain):
    request = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
    request.set_DomainName(domain)
    request.set_accept_format('json')
    try:
        result = ali_ctl.do_action_with_exception(request)
    except Exception as e:
        print('An error occurred! Error MSG: ')
        print(e)
        return []
    else:
        result = result.decode()
        result_dict = json.JSONDecoder().decode(result)
        result_list = result_dict['DomainRecords']['Record']
        result = []
        for i in result_list:
            if sub_domain == i['RR']:
                result.append(i['RecordId'])
                result.append(i['Value'])
                break
        return result


# 更新子域名信息
def update_dns(ali_ctl, sub_domain, dns_value, ttl, dns_record_id, ip_ver):
    request = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
    request.set_RR(sub_domain)
    request.set_Value(dns_value)
    request.set_RecordId(dns_record_id)
    request.set_TTL(ttl)
    request.set_accept_format('json')

    if ip_ver == 4:
        request.set_Type('A')
    else:
        request.set_Type('AAAA')

    result = ali_ctl.do_action_with_exception(request)
    return result


# 新增子域名解析
def add_dns(ali_ctl, dns_value, domain, sub_domain, ttl, ip_ver):
    request = AddDomainRecordRequest.AddDomainRecordRequest()
    request.set_DomainName(domain)
    request.set_RR(sub_domain)
    request.set_Value(dns_value)
    request.set_TTL(ttl)

    if ip_ver == 4:
        request.set_Type('A')
    else:
        request.set_Type('AAAA')

    result = ali_ctl.do_action_with_exception(request)
    return result


# 写入日志
def write_to_file(dns_value, dns_output):
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("{} {} {}".format(time_now, dns_value, dns_output))
    # write = open(sys.path[0] + '/aliyun_ddns.log', 'a')
    # write.write(time_now + ' ' + str(dns_value) + ' ' + dns_output + '\n')
    # write.close()


# 获取IP地址，支持v4与v6
def my_ip(i_ip_ver):
    if i_ip_ver == 4:
        get_ip_value = requests.get('http://whatismyip.akamai.com', timeout=30).content.decode().strip('\n')
    else:
        get_ip_value = requests.get('https://ipv6.ngx.hk', timeout=30).content.decode().strip('\n')
    return get_ip_value


def run_job():
    config_json = get_config_json()
    if (len(config_json) > 0):
        for v in config_json.values():
            rc_access_key_id = v['access_key_id']
            rc_access_key_secret = v['access_Key_secret']
            rc_domain = v['domain']
            rc_sub_domain = v['sub_domain']
            rc_ttl = v['ttl']
            ip_ver = v['ip_ver']
            current_ip = my_ip(ip_ver)

            clt = client.AcsClient(rc_access_key_id, rc_access_key_secret, 'cn-hangzhou')

            result_list = get_record_info(clt, rc_domain, rc_sub_domain)
            if len(result_list) == 0:
                aliyun_output = add_dns(clt, current_ip, rc_domain, rc_sub_domain, rc_ttl, ip_ver).decode()
                write_to_file(current_ip, aliyun_output)
            else:
                result_record_id = result_list[0]
                old_ip = result_list[1]
                if old_ip == current_ip:
                    print('The specified value of parameter Value is the same as old')
                else:
                    aliyun_output = update_dns(clt, rc_sub_domain, current_ip, rc_ttl, result_record_id, ip_ver).decode()
                    write_to_file(current_ip, aliyun_output)
    else:
        print("no config loaded, please recheck config file!")


# 运行
if __name__ == '__main__':
    schedule.every(60).seconds.do(run_job)  # 每10秒执行一次
    while True:
        schedule.run_pending()
        time.sleep(1)
