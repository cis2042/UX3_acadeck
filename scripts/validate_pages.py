#!/usr/bin/env python3
import os
import re
import sys
from urllib.parse import unquote

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Simple patterns to extract asset URLs (restrict to src|href)
ATTR_URL_RE = re.compile(r'''\b(?:src|href)\s*=\s*['\"]([^'\"]+)['\"]''', re.IGNORECASE)
CSS_URL_RE = re.compile(r'''url\(\s*['\"]?([^'\")]+)['\"]?\s*\)''', re.IGNORECASE)

def is_external(url: str) -> bool:
    return url.startswith('http://') or url.startswith('https://') or url.startswith('//')

def is_ignorable(url: str) -> bool:
    if not url or url.startswith('#'):
        return True
    if url.startswith('mailto:') or url.startswith('javascript:'):
        return True
    return False

def resolve_local_path(page_path: str, url: str):
    # Normalize relative vs root paths, try both encoded and decoded variants
    # Strip fragment (#...) to match filesystem names
    url_no_fragment = url.split('#', 1)[0]
    candidate = url_no_fragment
    if url.startswith('/'):
        candidate = os.path.join(ROOT, url_no_fragment.lstrip('/'))
    else:
        candidate = os.path.join(os.path.dirname(page_path), url_no_fragment)

    # Secure path resolution to prevent directory traversal
    candidate = os.path.abspath(candidate)
    decoded = os.path.abspath(unquote(candidate))

    # ROOT is already absolute via os.path.abspath
    if not (os.path.commonpath([ROOT, candidate]) == ROOT and os.path.commonpath([ROOT, decoded]) == ROOT):
        # Prevent directory traversal bypasses by returning a path that will fail existence checks
        return "/dev/null", "/dev/null"

    return candidate, decoded

ASSET_EXTS = (
    '.js', '.css', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico',
    '.xml', '.json', '.eot', '.ttf', '.woff', '.woff2', '.otf'
)

def looks_like_asset(url: str) -> bool:
    # Quick filter to avoid treating plain text values as paths
    return any(url.lower().split('#')[0].split('?')[0].endswith(ext) for ext in ASSET_EXTS)

def collect_urls(content: str):
    urls = []
    for m in ATTR_URL_RE.finditer(content):
        u = m.group(1)
        if looks_like_asset(u):
            urls.append(u)
    for m in CSS_URL_RE.finditer(content):
        u = m.group(1)
        if looks_like_asset(u):
            urls.append(u)
    return urls

def main():
    html_files = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        # Skip scripts directory
        if os.path.basename(dirpath) == 'scripts':
            continue
        for fname in filenames:
            if fname.lower().endswith('.html'):
                html_files.append(os.path.join(dirpath, fname))

    pages_with_issues = []
    external_refs = 0
    missing_locals = 0

    for page in sorted(html_files):
        try:
            with open(page, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            pages_with_issues.append((page, [f'read_error: {e}']))
            continue

        urls = collect_urls(content)
        problems = []
        for url in urls:
            if is_ignorable(url):
                continue
            if is_external(url):
                external_refs += 1
                # Flag only if it references acadeck.com specifically
                if 'acadeck.com' in url:
                    problems.append(f'external_acadeck_ref: {url}')
                continue
            # Local path
            candidate, decoded = resolve_local_path(page, url)
            if not (os.path.exists(candidate) or os.path.exists(decoded)):
                missing_locals += 1
                problems.append(f'missing_local_asset: {url}')

        if problems:
            pages_with_issues.append((page, problems))

    print(f'Total pages scanned: {len(html_files)}')
    print(f'External references total: {external_refs}')
    print(f'External acadeck.com refs: {sum(1 for _, probs in pages_with_issues for p in probs if p.startswith("external_acadeck_ref:"))}')
    print(f'Missing local assets total: {missing_locals}')
    print(f'Pages with issues: {len(pages_with_issues)}')

if __name__ == '__main__':
    main()