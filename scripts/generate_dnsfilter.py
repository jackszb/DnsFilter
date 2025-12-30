#!/usr/bin/env python3
import json
import re
import requests

# 下载 DnsFilter 列表
url = "https://raw.githubusercontent.com/AdguardTeam/HostlistsRegistry/main/filters/general/filter_1_DnsFilter/filter.txt"
response = requests.get(url)
response.raise_for_status()
lines = response.text.splitlines()

suffix = []
wildcard = []

# 提取域名
for line in lines:
    line = line.strip()
    if line.startswith("||") and not line.startswith("@@") and not line.startswith("/"):
        domain = re.sub(r'^\|\|', '', line)
        domain = re.sub(r'\^.*$', '', domain)
        domain = domain.strip()
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

# 生成 domain_regex.json，确保正则安全
domain_regex_list = []
for d in wildcard:
    # 将 * 转为 [^.]+，确保安全
    pattern = '^' + re.escape(d).replace(r'\*', r'[^.]+') + '$'
    # 修复可能的非法组合，如 [^.]+后跟特殊字符
    pattern = re.sub(r'\[\^.\]\+\.', r'[^.]+.', pattern)
    # 尝试编译正则，跳过无效正则
    try:
        re.compile(pattern)
        domain_regex_list.append(pattern)
    except re.error:
        print(f"跳过无效正则: {pattern}")

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

with open('DnsFilter.json', 'w') as f:
    json.dump(DnsFilter_json, f, indent=2)

print("DnsFilter.json, domain_regex.json, wildcard.txt, and suffix.txt generated successfully!")
