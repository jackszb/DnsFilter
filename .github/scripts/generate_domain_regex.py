#!/usr/bin/env python3
import re
import json

with open("wildcard.txt", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

regex_list = []

for dom in sorted(set(lines)):
    # 先按 * 拆分，逐段处理
    parts = dom.split("*")
    escaped_parts = [re.escape(p) for p in parts]

    # 用 DNS 语义的“单 label 通配”
    # * → [^.]+
    pattern = "[^.]+".join(escaped_parts)

    # 如果原始规则以 * 开头，允许多级前缀
    if dom.startswith("*"):
        pattern = r"(?:[^.]+\.)*" + pattern.lstrip(r"\.")

    # 如果原始规则以 * 结尾，允许尾部子域
    if dom.endswith("*"):
        pattern = pattern.rstrip(r"\.") + r"(?:\.[^.]+)*"

    regex_list.append(f"^{pattern}$")

output = {"domain_regex": regex_list}

with open("domain_regex.json", "w", encoding="utf-8") as out:
    json.dump(output, out, indent=2, ensure_ascii=False)

print(f"Generated {len(regex_list)} regex rules")
