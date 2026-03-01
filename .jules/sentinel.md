## 2024-05-14 - Security Header Implementation
**Vulnerability:** Missing Security Headers in vercel.json
**Learning:** The project relies on Vercel for deployment, and security headers like X-Frame-Options, X-Content-Type-Options, Strict-Transport-Security, and X-XSS-Protection were missing from the configuration. This leaves the static site vulnerable to clickjacking, MIME-sniffing, and other basic web attacks.
**Prevention:** Ensure `vercel.json` includes a standard set of security headers for all routes.
