#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).parent

SUFFIX_TXT = ROOT / "suffix.txt"
DOMAIN_SUFFIX_JSON = ROOT / "domain_suffix.json"
DOMAIN_REGEX_JSON = ROOT / "domain_regex.json"
OUTPUT_JSON = ROOT / "adguardfilter.json"

VERSION = 3


def load_suffix():
    if not SUFFIX_TXT.exists():
        return []

    suffixes = []
    with SUFFIX_TXT.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            suffixes.append(line)

    return sorted(set(suffixes))


def load_domain_regex():
    if not DOMAIN_REGEX_JSON.exists():
        return []

    with DOMAIN_REGEX_JSON.open("r", encoding="utf-8") as f:
        data = json.load(f)

    rules = data.get("rules", [])
    if not rules:
        return []

    return sorted(set(rules[0].get("domain_regex", [])))


def write_domain_suffix_json(suffixes):
    data = {
        "version": VERSION,
        "rules": [
            {
                "domain_suffix": suffixes
            }
        ]
    }

    DOMAIN_SUFFIX_JSON.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def write_adguardfilter_json(suffixes, domain_regex):
    rule = {}
    if suffixes:
        rule["domain_suffix"] = suffixes
    if domain_regex:
        rule["domain_regex"] = domain_regex

    data = {
        "version": VERSION,
        "rules": [rule]
    }

    OUTPUT_JSON.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def main():
    suffixes = load_suffix()
    domain_regex = load_domain_regex()

    write_domain_suffix_json(suffixes)
    write_adguardfilter_json(suffixes, domain_regex)


if __name__ == "__main__":
    main()
