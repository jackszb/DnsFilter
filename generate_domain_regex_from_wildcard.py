import re
import json

def clean_regex(regex):
    """
    清理正则表达式中的冗余部分，如多余的 .*
    """
    cleaned = re.sub(r'\.\*+', '.*', regex)  # 合并连续的 .* 为一个
    return cleaned

def wildcard_to_regex(domain):
    """
    根据通配符位置将域名转换为正则表达式。
    """
    # 如果通配符出现在域名的开头
    if domain.startswith("*"):
        domain = ".*" + domain[1:]  # 替换开头的 *
    
    # 如果通配符出现在域名的末尾
    elif domain.endswith("*"):
        domain = domain[:-1] + ".*"  # 替换结尾的 *
    
    # 如果通配符出现在域名的中间
    elif "*" in domain:
        domain = domain.replace("*", ".*")  # 替换中间的 *

    # 对于所有域名，加上 ^ 和 $ 来确保是全匹配
    return f"^{domain}$"

def process_wildcard_file(filename):
    """
    读取 wildcard.txt 文件，将其中的每个通配符域名转换为正则表达式。
    """
    with open(filename, "r") as file:
        lines = file.readlines()
        # 对每个域名应用 wildcard_to_regex 转换并清理冗余部分
        wildcard_domains = [clean_regex(wildcard_to_regex(line.strip())) for line in lines if line.strip()]
        return wildcard_domains

def generate_sing_box_rule(wildcard_domains):
    """
    生成 sing-box 规则文件，包含转换后的域名正则表达式。
    """
    return {"version": 3, "rules": [{"domain_regex": wildcard_domains}]}

def write_json_to_file(data, filename):
    """
    将生成的规则数据写入 JSON 文件。
    """
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

def main():
    wildcard_file = "wildcard.txt"  # 输入的 wildcard.txt 文件
    output_file = "domain_regex.json"  # 输出的 domain_regex.json 文件
    
    # 读取并转换域名
    wildcard_domains = process_wildcard_file(wildcard_file)

    # 生成 sing-box 规则文件
    rules = generate_sing_box_rule(wildcard_domains)
    
    # 写入 domain_regex.json 文件
    write_json_to_file(rules, output_file)

    # 打印生成的 domain_regex.json 文件内容确认
    with open(output_file, "r") as f:
        print(f.read())  # 打印生成的 domain_regex.json 文件内容

if __name__ == "__main__":
    main()
