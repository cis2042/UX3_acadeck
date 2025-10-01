部署指南（靜態網站）

目標：將 /Volumes/dev/Apps/acadeck 目錄部署為可公開存取的靜態站點。

一、快速部署到 Nginx（伺服器 / Docker 均可）
- 使用本目錄提供的 Dockerfile 與 nginx.conf：
  1) docker build -t acadeck-site -f deploy/Dockerfile .
  2) docker run -p 8080:80 acadeck-site
  3) 瀏覽 http://localhost:8080/
- 或在現有 Nginx 主機：
  1) 將整個專案目錄同步到伺服器，例如 /var/www/acadeck
  2) 使用 deploy/nginx.conf 作為範本，設定 root /var/www/acadeck;
  3) reload Nginx

注意：本專案目前路徑以網站根目錄為基準（/）。若未來部署在子目錄（例如 https://domain.com/site/），需先批次將所有以 / 開頭的資產路徑改為 /site/... 或將該子目錄設定為站點根（以獨立虛擬主機或子網域部署）。

二、部署到 Netlify（免伺服器）
- 新增站點，選擇「Deploy without Git」。
- 直接上傳整個專案目錄（或 deploy/acadeck-static.tar.gz 解壓後的內容）。
- Publish directory 設為專案根目錄（/）。

三、部署到 Vercel（免伺服器）
- 新建專案，選擇「Other」或「Static」。
- 將整個專案目錄上傳或連結 Git 後設定為靜態站點。

四、部署到 GitHub Pages（僅適用根網域）
- 由於本專案使用根相對路徑（/），建議以使用者頁面（user.github.io）或自訂網域部署於根目錄。
- 若使用專案頁面（user.github.io/repo），需先進行路徑前綴重寫。

五、已知事項
- 站內存在以百分比編碼表示的頁面連結（例如 index.html%3Fp=525.html）。多數標準伺服器會將 ? 視為查詢字串分隔符，可能導致深層連結行為與本地測試不同。若要完全保證跨主機一致性，建議後續進行「檔名重構」：
  - 將檔名中的 ? 改寫為安全字元或目錄結構（例如 index_p_525.html 或 p/525/index.html），並批次更新站內 href 連結。
  - 我們可提供自動化重構腳本以確保連結不受伺服器行為差異影響。