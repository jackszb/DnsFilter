import re
import json

def convert_wildcards_to_regex(domain):
    # 将 '*' 替换为 '.*' 以匹配任意字符
    domain = domain.replace("*", ".*")

    # 修正正则表达式：去掉域名中间的 ^ 和无效的 \2
    # 匹配域名的结尾部分，确保可以匹配子域名和顶级域名
    domain = re.sub(r"([^.]+)\.([a-z]+)$", r"^\1(\.[^.]+)*\.\2$", domain)

    # 确保正则表达式以 ^ 开头，以 $ 结尾
    if not domain.startswith("^"):
        domain = "^" + domain
    if not domain.endswith("$"):
        domain = domain + "$"

    return domain

def generate_sing_box_rule(domains):
    return {"version": 3, "rules": [{"domain_regex": [convert_wildcards_to_regex(domain) for domain in domains]}]}

def read_wildcard_file(filename):
    with open(filename, "r") as file:
        return [line.strip() for line in file.readlines() if line.strip()]

domains = read_wildcard_file("wildcard.txt")
rules = generate_sing_box_rule(domains)

with open("domain_regex.json", "w") as f:
    json.dump(rules, f, indent=2)
