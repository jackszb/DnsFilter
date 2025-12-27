#!/usr/bin/env python3
import re
import json

# 读取 cleaned wildcard 列表
with open("wildcard.txt", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

regex_list = []
for dom in sorted(set(lines)):
    # 转义 . 和其他正则特殊字符
    escaped = re.escape(dom)

    # 把原始的通配符 * 替换为正则量词 .*
    escaped = escaped.replace(r"\*", ".*")

    # 添加 ^ 和 $ 保证完整匹配
    pattern = f"^{escaped}$"
    regex_list.append(pattern)

# 输出 JSON
output = {"domain_regex": regex_list}
with open("domain_regex.json", "w", encoding="utf-8") as out:
    json.dump(output, out, indent=2, ensure_ascii=False)

print(f"Generated {len(regex_list)} regex rules")
