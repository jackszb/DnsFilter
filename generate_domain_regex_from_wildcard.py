import re
import json
import os

def convert_wildcards_to_regex(domain):
    """
    将域名中的通配符 '*' 转换为正则表达式形式。
    """
    # 如果域名以 '*' 开头，转换为 ^.*
    if domain.startswith("*"):
        domain = "^.*" + domain[1:]

    # 替换域名中间或其他位置的 '*' 为 .*
    domain = re.sub(r"\*", r".*", domain)

    # 如果 '*' 出现在后面，转换为 (\.[^.]+)*（匹配所有子域名和顶级域名）
    if domain.endswith(".*"):
        domain = domain[:-2] + "(\.[^.]+)*$"
    elif not domain.endswith("$"):
        domain = domain + "$"
    
    return domain

def generate_sing_box_rule(domains):
    """
    根据输入的域名列表生成 sing-box 规则。
    """
    return {"version": 3, "rules": [{"domain_regex": [convert_wildcards_to_regex(domain) for domain in domains]}]}

def read_wildcard_file(filename):
    """
    读取 wildcard.txt 文件，返回所有非空行的域名列表。
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"{filename} not found!")
    
    with open(filename, "r") as file:
        lines = file.readlines()
        return [line.strip() for line in lines if line.strip()]

def write_json_to_file(data, filename):
    """
    将生成的规则数据写入 JSON 文件，覆盖原文件。
    """
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

def main():
    wildcard_file = "wildcard.txt"  # 输入的 wildcard.txt 文件
    output_file = "domain_regex.json"  # 输出的 domain_regex.json 文件
    
    # 读取 wildcard.txt 文件中的域名
    try:
        domains = read_wildcard_file(wildcard_file)
        print(f"Read {len(domains)} domains from {wildcard_file}")
    except FileNotFoundError as e:
        print(e)
        return

    # 生成 sing-box 规则文件
    rules = generate_sing_box_rule(domains)
    
    # 写入 domain_regex.json 文件
    write_json_to_file(rules, output_file)
    print(f"Generated {output_file}")

    # 打印生成的 domain_regex.json 文件内容确认
    with open(output_file, "r") as f:
        print(f.read())  # 打印生成的 domain_regex.json 文件内容

if __name__ == "__main__":
    main()
