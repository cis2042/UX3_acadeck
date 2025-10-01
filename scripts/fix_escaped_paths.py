#!/usr/bin/env python3
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

TARGET_EXTS = {'.html', '.js'}

def should_process(path: str) -> bool:
    _, ext = os.path.splitext(path.lower())
    return ext in TARGET_EXTS and 'scripts' not in os.path.dirname(path)

def fix_content(text: str) -> str:
    # Normalize escaped slashes in root-relative paths like \/wp-includes -> /wp-includes
    return text.replace('/\\/', '/')

def main():
    changed_files = 0
    total_replacements = 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        if os.path.basename(dirpath) == 'scripts':
            continue
        for fname in filenames:
            path = os.path.join(dirpath, fname)
            if not should_process(path):
                continue
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            except Exception:
                continue
            fixed = fix_content(content)
            if fixed != content:
                try:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(fixed)
                    changed_files += 1
                    # Rough count
                    total_replacements += fixed.count('/\\/')
                except Exception:
                    pass
    print(f'Changed files: {changed_files}')
    print(f'Replacements applied: {total_replacements}')

if __name__ == '__main__':
    main()