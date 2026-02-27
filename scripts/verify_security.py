#!/usr/bin/env python3
import json
import os
import sys

def check_vercel_headers():
    vercel_path = 'vercel.json'
    if not os.path.exists(vercel_path):
        print(f"Error: {vercel_path} not found.")
        return False

    try:
        with open(vercel_path, 'r') as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse {vercel_path}: {e}")
        return False

    headers_config = config.get('headers', [])
    if not headers_config:
        print("Error: No 'headers' section found in vercel.json.")
        return False

    required_headers = {
        'X-Frame-Options',
        'X-Content-Type-Options',
        'X-XSS-Protection',
        'Referrer-Policy',
        'Permissions-Policy'
    }

    found_headers = set()

    # Check all header rules
    for rule in headers_config:
        for header in rule.get('headers', []):
            key = header.get('key')
            if key in required_headers:
                found_headers.add(key)

    missing_headers = required_headers - found_headers
    if missing_headers:
        print(f"Error: Missing security headers in vercel.json: {', '.join(missing_headers)}")
        return False

    print("Success: All required security headers found in vercel.json.")
    return True

def check_banned_files():
    banned_files = [
        'xmlrpc.php',
        'xmlrpc.php?rsd'
    ]

    found_banned = []
    for f in banned_files:
        if os.path.exists(f):
            found_banned.append(f)

    if found_banned:
        print(f"Error: Banned files found: {', '.join(found_banned)}")
        return False

    print("Success: No banned files found.")
    return True

def main():
    headers_ok = check_vercel_headers()
    files_ok = check_banned_files()

    if headers_ok and files_ok:
        print("\n✅ Security check passed!")
        sys.exit(0)
    else:
        print("\n❌ Security check failed!")
        sys.exit(1)

if __name__ == '__main__':
    main()
