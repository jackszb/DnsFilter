import re
import json

def wildcard_to_regex(domain):
    """
    将含有通配符 '*' 的域名转换为正则表达式。
    - 如果通配符在开头，转换为 ^.*domain$
    - 如果通配符在末尾，转换为 ^domain.*$
    - 如果通配符在中间，转换为 domain.*domain
    """
    if domain.startswith("*"):
        # 通配符在开头
        domain = "^.*" + domain[1:]  # 替换开头的 *
    elif domain.endswith("*"):
        # 通配符在结尾
        domain = domain[:-1] + ".*$"  # 替换结尾的 *
    elif "*" in domain:
        # 通配符在中间
        domain = domain.replace("*", ".*")  # 替换中间的 *
    
    # 添加正则表达式的起始和结束标记
    return domain

def clean_regex(regex):
    """
    清理冗余的部分，例如多个 .* 合并为一个。
    """
    return re.sub(r'\.\*+', '.*', regex)

def process_wildcard_file(filename):
    """
    处理 wildcard.txt 文件，转换其中的域名通配符为正则表达式。
    """
    with open(filename, "r") as file:
        lines = file.readlines()
        wildcard_domains = [clean_regex(wildcard_to_regex(line.strip())) for line in lines if line.strip()]
        return wildcard_domains

def generate_sing_box_rule(wildcard_domains):
    """
    根据转换后的正则表达式生成 sing-box 规则。
    """
    return {"version": 3, "rules": [{"domain_regex": wildcard_domains}]}

def write_json_to_file(data, filename):
    """
    将数据写入 JSON 文件。
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

    # 打印生成的 domain_regex.json 文件内容
    with open(output_file, "r") as f:
        print(f.read())  # 打印生成的 domain_regex.json 文件内容

if __name__ == "__main__":
    main()
