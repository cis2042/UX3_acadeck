#!/usr/bin/env python3
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

TARGET_EXTS = {'.html', '.php', '.js', '.xml'}

# Patterns to remove entire tags/lines referencing acadeck.com
OEMBED_TAG_RE = re.compile(r"^\s*<link[^>]+rest_route[^>]+acadeck\.com[^>]*>\s*$", re.IGNORECASE)

# AddToAny share links – replace encoded acadeck.com with empty (relative path only)
ADD2ANY_RE = re.compile(r"(https://www\.addtoany\.com/add_to/[^?]+\?[^\s>'\"]*linkurl=)(?:https?%3A%2F%2Facadeck\.com%2F)", re.IGNORECASE)

# Plain acadeck.com occurrences (fallback)
PLAIN_DOMAIN_RE = re.compile(r"https?://acadeck\.com", re.IGNORECASE)

# Escaped JSON/JS strings containing acadeck.com
ESCAPED_DOMAIN_RE = re.compile(r"https?:\\/\\/acadeck\\.com", re.IGNORECASE)

def should_process(path: str) -> bool:
    _, ext = os.path.splitext(path.lower())
    return ext in TARGET_EXTS and '/scripts/' not in path.replace('\\', '/')

def process_content(text: str) -> str:
    lines = text.splitlines()
    new_lines = []
    removed = 0

    for ln in lines:
        if OEMBED_TAG_RE.search(ln):
            removed += 1
            continue
        # Fix AddToAny linkurl – drop domain, keep relative path
        ln_fixed = ADD2ANY_RE.sub(r"\1", ln)
        # Remove plain and escaped domain leftovers
        ln_fixed = PLAIN_DOMAIN_RE.sub('', ln_fixed)
        ln_fixed = ESCAPED_DOMAIN_RE.sub('', ln_fixed)
        new_lines.append(ln_fixed)

    return "\n".join(new_lines)

def main():
    changed = 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        for fname in filenames:
            path = os.path.join(dirpath, fname)
            if not should_process(path):
                continue
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            except Exception:
                continue
            fixed = process_content(content)
            if fixed != content:
                try:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(fixed)
                    changed += 1
                except Exception:
                    pass
    print(f'Files changed: {changed}')

if __name__ == '__main__':
    main()