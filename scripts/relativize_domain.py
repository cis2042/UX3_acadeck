#!/usr/bin/env python3
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Domain variants to normalize
DOMAINS = [
    'http://acadeck.com',
    'https://acadeck.com',
    '//acadeck.com',
    'http://www.acadeck.com',
    'https://www.acadeck.com',
    '//www.acadeck.com',
    # Escaped variants inside JSON/JS (e.g., http:\/\/acadeck.com)
    'http:\\/\\/acadeck.com',
    'https:\\/\\/acadeck.com',
    'http:\\/\\/www.acadeck.com',
    'https:\\/\\/www.acadeck.com',
]

def should_process_file(path: str) -> bool:
    # Process likely text files. Many files have '?' in names; do not rely on extension only.
    # Skip binary font files and obvious binaries.
    lower = path.lower()
    if any(lower.endswith(ext) for ext in [
        '.eot', '.ttf', '.woff', '.woff2', '.otf', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.pdf', '.zip'
    ]):
        return False
    return True

def relativize_content(content: str) -> tuple[str, int]:
    count = 0
    for d in DOMAINS:
        if d in content:
            # Replace domain with root '/'
            occurrences = content.count(d)
            content = content.replace(d, '/')
            count += occurrences
    return content, count

def main():
    target_root = ROOT
    changed_files = 0
    total_replacements = 0

    for dirpath, dirnames, filenames in os.walk(target_root):
        # Skip the scripts directory itself
        if os.path.basename(dirpath) == 'scripts':
            continue
        for fname in filenames:
            fpath = os.path.join(dirpath, fname)
            # Safety: skip this script if found elsewhere
            if fpath.endswith('relativize_domain.py'):
                continue
            if not should_process_file(fpath):
                continue
            try:
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                    original = f.read()
                new_content, count = relativize_content(original)
                if count > 0 and new_content != original:
                    with open(fpath, 'w', encoding='utf-8', errors='ignore') as f:
                        f.write(new_content)
                    changed_files += 1
                    total_replacements += count
            except Exception as e:
                # Non-fatal: print to stderr and continue
                print(f"[skip] {fpath}: {e}", file=sys.stderr)

    print(f"Updated files: {changed_files}, total replacements: {total_replacements}")

if __name__ == '__main__':
    main()