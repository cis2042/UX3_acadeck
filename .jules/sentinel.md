## 2024-05-24 - [Remove WordPress Artifacts]
**Vulnerability:** Leftover WordPress API files (e.g. `xmlrpc.php`, `index.php?rest_route=/`) expose APIs that are potentially vulnerable to exploits like brute force attacks or XML-RPC amplification attacks, especially since the site is now purely static.
**Learning:** Even when a site is staticized, files from the original dynamic CMS might remain and present an attack surface if served by the web server.
**Prevention:** Automatically clean up standard CMS API entry points during the staticization process.
## 2024-05-24 - [Add Security Headers to Vercel config]
**Vulnerability:** Missing security headers allowed potential attacks like Clickjacking, XSS, and MIME-type sniffing.
**Learning:** Static sites deployed via Vercel need security headers explicitly defined in `vercel.json` to enforce security policies.
**Prevention:** Always include a baseline set of security headers (`X-Frame-Options`, `X-Content-Type-Options`, `X-XSS-Protection`, `Referrer-Policy`) in Vercel or other CDN deployment configurations.
