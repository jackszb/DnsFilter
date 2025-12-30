#!/usr/bin/env python3
import json
import re
import requests

# 下载 DnsFilter 列表
url = "https://raw.githubusercontent.com/AdguardTeam/HostlistsRegistry/main/filters/general/filter_1_DnsFilter/filter.txt"
response = requests.get(url)
response.raise_for_status()
lines = response.text.splitlines()

# 分离通配符域名和普通后缀
suffix = []
wildcard = []

for line in lines:
    line = line.strip()
    if line.startswith("||") and not line.startswith("@@") and not line.startswith("/"):
        domain = re.sub(r'^\|\|', '', line)
        domain = re.sub(r'\^.*$', '', domain)
        if not domain:
            continue
        if re.match(r'^([0-9]{1,3}\.){1,3}[0-9]{1,3}$', domain):
            continue
        if '*' in domain:
            wildcard.append(domain)
        else:
            suffix.append(domain)

# 保存 wildcard.txt 和 suffix.txt
with open('wildcard.txt', 'w') as f:
    f.write('\n'.join(sorted(set(wildcard))))
with open('suffix.txt', 'w') as f:
    f.write('\n'.join(sorted(set(suffix))))

# 生成 domain_regex.json
def is_valid_domain(d):
    if '..' in d or d.startswith('.') or d.endswith('.') or len(d) < 3:
        return False
    if re.search(r'[^a-zA-Z0-9\-\*\.]', d):
        return False
    return True

domain_regex_list = ['^' + re.escape(d).replace(r'\*', r'[^.]+') + '$' 
                     for d in wildcard if is_valid_domain(d)]
domain_regex_list = sorted(set(domain_regex_list))

with open('domain_regex.json', 'w') as f:
    json.dump({'domain_regex': domain_regex_list}, f, indent=2)

# 生成最终 DnsFilter.json
DnsFilter_json = {
    "version": 3,
    "rules": [
        {
            "domain_suffix": sorted(set(suffix)),
            "domain_regex": domain_regex_list
        }
    ]
}

with open('DnsFilter.json', 'w') as f:
    json.dump(DnsFilter_json, f, indent=2)

print("DnsFilter.json, domain_regex.json, wildcard.txt, and suffix.txt generated successfully!")
