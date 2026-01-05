import re

suffix = []   # 精确域名（不含通配符）
wildcard = [] # 包含通配符的域名

# 读取过滤列表
with open('filter.txt', 'r') as f:
    lines = f.readlines()

# 定义忽略规则：四类
ignore_patterns = [
    # 第一类：精确 IP 地址
    re.compile(r'^\|\|(\d{1,3}\.){3}\d{1,3}\^'),
    
    # 第二类：正则表达式形式的 IP 地址
    re.compile(r'^\/\^.*\^\/$'),
    
    # 第三类：带通配符的 GIF 文件
    re.compile(r'.*\*.*\.gif$'),
    
    # 第四类：以 @@ 开头的排除规则
    re.compile(r'^\@\@')
]

# 提取域名
for line in lines:
    line = line.strip()

    # 如果匹配忽略规则，跳过当前行
    if any(pattern.match(line) for pattern in ignore_patterns):
        continue
    
    # 精确域名（domain_suffix）
    if line.startswith('||'):
        domain = re.sub(r'^\|\|', '', line)
        domain = re.sub(r'\^.*$', '', domain).strip()
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

print('suffix.txt and wildcard.txt generated successfully!')
