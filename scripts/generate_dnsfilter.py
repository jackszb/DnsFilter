#!/usr/bin/env python3
import json
import re
import requests

# 下载 DnsFilter 列表
url = "https://raw.githubusercontent.com/AdguardTeam/HostlistsRegistry/main/filters/general/filter_1_DnsFilter/filter.txt"
response = requests.get(url)
response.raise_for_status()
lines = response.text.splitlines()

# 需要排除的特殊域名/IP
exclude_list = [
    "*.gif",
    "107.167.*.*",
    "121.204.246.*",
    "38.33.15.*",
    "67.21.92.*"
]

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
        # 排除纯数字或 IP 开头的域名（仅对 domain_regex 适用）
        if re.match(r'^(\d{1,3}\.){1,3}\d{1,3}$', domain):  # 排除 IP 地址
            continue
        # 排除非法字符和长度问题
        if '..' in domain or domain.startswith('.') or domain.endswith('.') or len(domain) < 3:
            continue
        if re.search(r'[^a-zA-Z0-9\-.*]', domain):
            continue
        # 精确域名 (domain_suffix)
        if '*' not in domain:
            suffix.append(domain)
        else:
            wildcard.append(domain)

# 去重排序
suffix = sorted(set(suffix))
wildcard = sorted(set(wildcard))

# 保存 txt 文件
with open('suffix.txt', 'w') as f:
    f.write('\n'.join(suffix))
with open('wildcard.txt', 'w') as f:
    f.write('\n'.join(wildcard))

# 生成 domain_regex.json
domain_regex_list = []
for d in wildcard:
    # 排除数字开头的域名
    if re.match(r'^\d', d):
        continue
    # 排除特殊域名/IP
    if any(d.startswith(e.replace('*', '')) for e in exclude_list):
        continue
    # 转换通配符为科学正则表达式
    escaped = re.escape(d).replace(r'\*', r'[^.]+')
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
