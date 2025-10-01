FROM nginx:alpine

# 將網站檔案拷貝到 Nginx 預設靜態目錄
COPY . /usr/share/nginx/html
# 覆蓋預設站台設定
COPY deploy/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]