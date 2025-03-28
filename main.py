from fastapi import FastAPI
from pydantic import BaseModel
from celery_app import snap_images_task

app = FastAPI()


# post 请求
class UserResponse(BaseModel):
    status: int
    data: str


class Target(BaseModel):
    url: str
    proxy: str = None


@app.post("/snap_site_picture")
def snap_site_picture(target: Target):
    # 判断是否为 url
    if not target.url.startswith("http"):
        return UserResponse(status=400, data="URL不合法")

    if target.proxy:
        if not target.proxy.startswith("http"):
            return UserResponse(status=400, data="代理地址不合法")
    # 进行截图
    snap_task = snap_images_task.delay(target.url, timeout=30, proxy=target.proxy)

    try:
        result = snap_task.get(timeout=35)  # 同步等待任务完成
    except Exception as e:
        result = ["error", str(e)]

    if result[0] == "error":
        return UserResponse(status=400, data=result[1])

    image_url = result[1]
    return UserResponse(status=200, data=image_url)
