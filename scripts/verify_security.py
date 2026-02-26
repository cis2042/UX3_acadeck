import os
import json
import glob

def check_vercel_headers():
    if not os.path.exists('vercel.json'):
        print("❌ vercel.json not found")
        return False

    try:
        with open('vercel.json', 'r') as f:
            config = json.load(f)

        headers = config.get('headers', [])
        if not headers:
            print("❌ No headers configured in vercel.json")
            return False

        security_headers = [
            "X-Content-Type-Options",
            "X-Frame-Options",
            "X-XSS-Protection",
            "Referrer-Policy",
            "Permissions-Policy"
        ]

        found_count = 0
        for rule in headers:
            for header in rule.get('headers', []):
                if header['key'] in security_headers:
                    found_count += 1

        if found_count >= 3: # Expecting at least a few
            print("✅ Security headers found in vercel.json")
            return True
        else:
            print(f"❌ Only {found_count} security headers found")
            return False

    except Exception as e:
        print(f"❌ Error parsing vercel.json: {e}")
        return False

def check_exposed_files():
    # Check for xmlrpc.php (and variants like xmlrpc.php?rsd)
    xmlrpc = glob.glob('xmlrpc.php*')

    # Check for rest route files
    rest_routes = glob.glob('index.php?rest_route=*')

    if xmlrpc or rest_routes:
        print(f"❌ Exposed files found: {len(xmlrpc)} xmlrpc, {len(rest_routes)} rest_routes")
        return False
    else:
        print("✅ No exposed WordPress artifact files found")
        return True

if __name__ == "__main__":
    print("Running Security Verification...")
    headers_ok = check_vercel_headers()
    files_ok = check_exposed_files()

    if headers_ok and files_ok:
        print("\n🎉 All security checks passed!")
        exit(0)
    else:
        print("\n⚠️ Security checks failed.")
        exit(1)
