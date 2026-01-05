import re
import json

def clean_regex(regex):
    """
    清理不必要的重复 .*
    """
    # 清理多余的 .* ，只保留一个
    cleaned = re.sub(r'\.\*+', '.*', regex)
    # 修复类似 'aan.amazon..*$' 为 'aan.amazon.*$'
    cleaned = re.sub(r'\.\*\.', '.*.', cleaned)
    print(f"Cleaned regex: {cleaned}")  # 调试输出
    return cleaned

def process_wildcard_file(filename):
    """
    读取 wildcard.txt 文件，将其中的每个通配符域名转换为正则表达式。
    """
    with open(filename, "r") as file:
        lines = file.readlines()
        # 对每个域名应用 wildcard_to_regex 转换并清理冗余部分
        wildcard_domains = [clean_regex(wildcard_to_regex(line.strip())) for line in lines if line.strip()]
        print(f"Converted domains: {wildcard_domains}")  # 调试输出
        return wildcard_domains

def wildcard_to_regex(domain):
    """
    将域名中的 '*' 替换为正则表达式中的 '.*'，用于匹配任意字符。
    """
    domain = domain.replace('*', '.*')  # 将 * 替换为 .*
    print(f"Wildcard to regex: {domain}")  # 调试输出
    return f"^{domain}$"

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
    print(f"JSON written to {filename}")  # 调试输出

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
