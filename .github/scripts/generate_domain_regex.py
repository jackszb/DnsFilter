#!/usr/bin/env python3
import re
import json

WILDCARD_FILE = "wildcard.txt"
REGEX_OUT = "domain_regex.json"
SUFFIX_OUT = "suffix_from_wildcard.txt"

regex_rules = []
suffix_rules = set()

def is_valid_domain(dom: str) -> bool:
    if dom.endswith("."):
        return False
    if ".." in dom:
        return False
    return True

def is_tld_wildcard(dom: str) -> bool:
    # amazon.* / example.* / foo.bar.*
    return dom.count(".") <= 1

with open(WILDCARD_FILE, encoding="utf-8") as f:
    domains = sorted(set(line.strip() for line in f if line.strip()))

for dom in domains:
    if not is_valid_domain(dom):
        continue

    if dom.count("*") == 0:
        continue

    # 丢弃多 * 规则（危险 + 复杂）
    if dom.count("*") > 1:
        continue

    labels = dom.split(".")

    # *.example.com → suffix
    if labels[0] == "*":
        suffix_rules.add(".".join(labels[1:]))
        continue

    # TLD 泛化 → 丢弃
    if is_tld_wildcard(dom):
        continue

    label_with_star = [l for l in labels if "*" in l]

    # * 单独作为 label（如 a.*.b.com）→ 丢弃
    if any(l == "*" for l in label_with_star):
        continue

    # 只允许 1 个 label 含 *
    if len(label_with_star) != 1:
        continue

    # 构造 regex
    regex_labels = []
    for l in labels:
        if "*" in l:
            escaped = re.escape(l).replace(r"\*", "[^.]+")
            regex_labels.append(escaped)
        else:
            regex_labels.append(re.escape(l))

    pattern = "^" + r"\.".join(regex_labels) + "$"
    regex_rules.append(pattern)

# 输出 regex
with open(REGEX_OUT, "w", encoding="utf-8") as f:
    json.dump(
        {"domain_regex": sorted(set(regex_rules))},
        f,
        indent=2,
        ensure_ascii=False
    )

# 输出降级 suffix
with open(SUFFIX_OUT, "w", encoding="utf-8") as f:
    for s in sorted(suffix_rules):
        f.write(s + "\n")

print(f"Generated {len(regex_rules)} domain_regex rules")
print(f"Generated {len(suffix_rules)} suffix rules from wildcard")
