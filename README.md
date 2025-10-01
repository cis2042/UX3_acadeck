# Acadeck 靜態網站

靜態化的 WordPress 網站，已移除過時的網域引用（acadeck.com）、調整資產載入路徑，並提供多種部署方式：GitHub Pages、Vercel、Netlify、Docker/Nginx。本倉庫已配置 GitHub Actions 便於自動部署。

## 快速開始（本地預覽）
- 需求：系統已安裝 Python 3
- 在專案根目錄啟動簡易伺服器：
  ```bash
  python3 -m http.server 8000
  ```
- 開啟瀏覽器：`http://localhost:8000/index.html`

## GitHub Pages 部署
本倉庫已包含工作流程檔：`.github/workflows/pages.yml`。

- 推送到 GitHub（已完成者可跳過）：
  ```bash
  git remote add origin https://github.com/cis2042/acadeck.git
  git branch -M main
  git push -u origin main
  ```
- 啟用 Pages：到倉庫 Settings → Pages → Source 選擇「GitHub Actions」。
- 部署完成後預設網址：`https://cis2042.github.io/acadeck/`

### 專案頁面與路徑前綴注意
- 本站資產多為「根相對路徑」（以 `/` 開頭）。若部署在專案頁面（`https://{user}.github.io/{repo}/`），`/wp-includes/...` 會指向根域而非子路徑，導致資產 404。
- 解法：
  - 使用「使用者頁面」倉庫（`cis2042.github.io`），網址即為根域，現有路徑可直接使用；或
  - 將所有以 `/` 開頭的資產與連結批次加上前綴（例如 `/acadeck/...`），並同步更新 `canonical`、`og:url`、分享連結 `linkurl` 等。我可以提供重寫腳本來自動處理。

## Vercel 部署
本倉庫含 `vercel.json`，可直接部署。
- 使用 CLI：
  ```bash
  npm i -g vercel
  vercel
  vercel deploy --prod
  ```
- 綁定網域：在 Vercel 專案的 Domains 加入你的網域，DNS 設定 A 記錄到 `76.76.21.21`（apex），或 CNAME 到 `cname.vercel-dns.com`（子網域）。

## Netlify 部署
- 新增站點，選擇「Deploy without Git」（上傳整個目錄）或連接 GitHub 倉庫。
- 網域管理：子網域以 CNAME 指向 `*.netlify.app`；根網域建議使用 Netlify DNS 或 DNS 支援 ALIAS/ANAME。

## Docker/Nginx 部署
已提供 Nginx 配置與 Dockerfile（位於 `deploy/`）。
- 建置容器：
  ```bash
  docker build -t acadeck -f deploy/Dockerfile .
  docker run -d -p 8080:80 --name acadeck acadeck
  # 瀏覽 http://localhost:8080/
  ```
- 直接使用 Nginx：
  - 將網站檔案放置於伺服器目錄（例如 `/var/www/html`）。
  - 套用 `deploy/nginx.conf`（依你的路徑調整 `root` 與 `server_name`）。
  - 測試並重載：
    ```bash
    sudo nginx -t && sudo systemctl reload nginx
    ```
- HTTPS：使用 Let’s Encrypt/Certbot：
  ```bash
  sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
  ```

## 自訂網域
- GitHub Pages：在倉庫 Pages 設定自訂網域並新增 `CNAME` 記錄指向 `{user}.github.io`。
- Vercel：新增網域後依指示建立 A/CNAME；自動簽發憑證。
- Netlify：在 Domain management 綁定網域；自動簽發憑證。

## 相容性與路徑說明
- `.nojekyll` 已加入，避免 GitHub Pages 的 Jekyll 處理造成路徑與檔名問題。
- 站內部分頁面檔名含 URL 編碼或 `?`，在部分 CDN/瀏覽器上可能有相容性差異；若需要，我可以將深連結頁面重構為目錄化路徑（例如 `index.html?p=525.html` → `p/525/index.html`），並批次更新站內連結與中繼資料。

## 內建工具腳本（scripts/）
- `validate_pages.py`：掃描頁面資產引用並回報缺失或外部依賴。
  ```bash
  python3 scripts/validate_pages.py
  ```
- `fix_escaped_paths.py`：清理路徑中的不必要跳脫斜線，避免瀏覽器誤判為協定相對 URL。
  ```bash
  python3 scripts/fix_escaped_paths.py
  ```
- `remove_acadeck_refs.py`：移除或改寫 `acadeck.com` 引用，清理 oEmbed 連結與分享連結參數。
  ```bash
  python3 scripts/remove_acadeck_refs.py
  ```
- `relativize_domain.py`：提供把絕對域名改為相對路徑的輔助函式（可擴充為前綴重寫工具）。

## 專案結構（摘要）
- 根目錄包含大量靜態頁：`index.html?p=XXX.html` 等。
- WordPress 靜態資產：`wp-includes/`、`wp-content/`（主題、插件、uploads）。
- 部署與設定：`.github/workflows/pages.yml`、`.nojekyll`、`deploy/`、`vercel.json`。

## 常見問題
- 問：為何 GitHub Pages 專案頁面資產載入 404？
  - 答：因為根相對路徑以 `/` 開頭，需改為加上子路徑前綴或改用使用者頁面倉庫。
- 問：外部網域請求錯誤（如 `net::ERR_NAME_NOT_RESOLVED`）？
  - 答：已清除舊網域引用；若仍有外部資產請提供網址，我將批次改寫為本地或移除。

## 聯絡/維護
- 若要改用新網域或子目錄部署，請提供最終網址與期望的路徑前綴，我可為你批次重寫路徑與中繼資料，並驗證部署後視覺與資產載入是否正常。