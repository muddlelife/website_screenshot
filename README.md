# website_screenshot
利用fastapi和playwright对指定网页进行截图，支持http代理

# 部署方式

## 1.安装redis-server
```shell
sudo apt-get update
sudo apt-get install redis-server
```

## 2.在项目根目录下创建python虚拟环境
```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium # 安装 chromium 浏览器
```

## 3. 启动celery任务
```shell
celery -A celery_app worker --loglevel=info --logfile=logs.txt
```
## 4.启动fastapi
```shell
uvicorn main:app --reload
```

# 接口使用方式

## 请求（无代理）
```shell
curl --request POST \
  --url http://127.0.0.1:8000/snap_site_picture \
  --header 'Accept: */*' \
  --header 'Accept-Encoding: gzip, deflate, br' \
  --header 'Connection: keep-alive' \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:136.0) Gecko/20100101 Firefox/136.0' \
  --data '{
    "url":"https://www.baidu.com",
}'
```
## 请求（有代理）
```shell
curl --request POST \
  --url http://127.0.0.1:8000/snap_site_picture \
  --header 'Accept: */*' \
  --header 'Accept-Encoding: gzip, deflate, br' \
  --header 'Connection: keep-alive' \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:136.0) Gecko/20100101 Firefox/136.0' \
  --data '{
    "url":"https://www.baidu.com",
    "proxy":"http://127.0.0.1:7890"
}'
```
## 响应
```json
{
	"status": 200,
	"data": "./picture/www_baidu_com_2025_03_28_11_38_39.png"
}
```