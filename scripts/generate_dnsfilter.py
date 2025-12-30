#!/usr/bin/env python3
import json
import re
import requests

# 下载 DnsFilter 列表
url = "https://raw.githubusercontent.com/AdguardTeam/HostlistsRegistry/main/filters/general/filter_1_DnsFilter/filter.txt"
response = requests.get(url)
response.raise_for_status()
lines = response.text.splitlines()

suffix = []   # 精确域名（不含通配符）
wildcard = [] # 包含通配符的域名

# 提取域名
for line in lines:
    line = line.strip()
    if not line or line.startswith("@@") or line.startswith("/"):
        continue
    if line.startswith("||"):
        domain = re.sub(r'^\|\|', '', line)
        domain = re.sub(r'\^.*$', '', domain).strip()
        if not domain:
            continue
        # 排除纯数字或 IP 开头
        if re.match(r'^(\d{1,3}\.){1,3}\d{1,3}$', domain):
            continue
        if re.match(r'^\d', domain):
            continue
        # 排除连续点或非法字符
        if '..' in domain or domain.startswith('.') or domain.endswith('.') or len(domain) < 3:
            continue
        if re.search(r'[^a-zA-Z0-9\-.*]', domain):
            continue
        if '*' in domain:
            wildcard.append(domain)
        else:
            suffix.append(domain)

# 去重排序
suffix = sorted(set(suffix))
wildcard = sorted(set(wildcard))

# 保存 txt 文件
with open('suffix.txt', 'w') as f:
    f.write('\n'.join(suffix))
with open('wildcard.txt', 'w') as f:
    f.write('\n'.join(wildcard))

# 生成 domain_regex.json
# 使用科学正则，匹配一级及以上子域名（多级也能匹配）
domain_regex_list = []
for d in wildcard:
    # 转换通配符为正则表达式：替换 '*' 为 '[^.]+'
    escaped = re.escape(d).replace(r'\*', r'[^.]+')

    # 自动加上多级匹配：支持 abc.example.com 和 x.y.example.com
    # 比如 "*-datareceiver.aki-game.net" 会变成 "^([^.]+\.)*-datareceiver.aki-game.net$"
    regex = r'^([^.]+\.)*' + escaped + r'$'
    domain_regex_list.append(regex)

domain_regex_list = sorted(set(domain_regex_list))

# 保存 domain_regex.json
with open('domain_regex.json', 'w') as f:
    json.dump({'domain_regex': domain_regex_list}, f, indent=2)

# 生成最终 DnsFilter.json
DnsFilter_json = {
    "version": 3,
    "rules": [
        {
            "domain_suffix": suffix,
            "domain_regex": domain_regex_list
        }
    ]
}

# 保存 DnsFilter.json
with open('DnsFilter.json', 'w') as f:
    json.dump(DnsFilter_json, f, indent=2)

print("DnsFilter.json, domain_regex.json, wildcard.txt, and suffix.txt generated successfully!")
