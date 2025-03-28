from celery import Celery
from playwright.sync_api import Playwright, sync_playwright
from urllib.parse import urlparse
from datetime import datetime
import uuid

# 创建celery实例
celery_app = Celery(
    "celery_app",
    broker="redis://127.0.0.1:6379/0",
    backend="redis://127.0.0.1:6379/1",
    broker_connection_retry_on_startup=True,
)

celery_app.conf.update(
    worker_max_tasks_per_child=50,
    result_expires=3600,  # 结果过期时间 (秒)
)


# 生成uuid
def generate_32bit_uuid():
    # 生成一个UUID对象
    full_uuid = uuid.uuid4()
    # 转换为32位的十六进制字符串
    uuid_32bit = full_uuid.hex
    return uuid_32bit


# 根据URL生成图片名称
def get_image_name(url):
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.replace(".", "_")
        now = datetime.now()
        date_str = now.strftime("%Y_%m_%d_%H_%M_%S")
        filename = f"{domain}_{date_str}.png"
        return filename
    except:
        return generate_32bit_uuid() + ".png"


def snap_images(playwright: Playwright, url, timeout, proxy):
    browser = playwright.chromium.launch(
        headless=True, args=["--explicitly-allowed-ports=1-65535"]
    )

    if proxy:
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            ignore_https_errors=True,  # 忽略证书错误
            proxy={
                "server": proxy,
            },
        )
    else:
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            ignore_https_errors=True,  # 忽略证书错误
        )

    page = context.new_page()
    try:
        page.goto(url, timeout=timeout * 1000)
        # 设置网络闲置
        page.wait_for_load_state("networkidle")
    except Exception as e:
        return "error", "page error: {}".format(str(e))
    screenshot_path = "./picture/{}".format(get_image_name(url))
    page.screenshot(path=screenshot_path)
    context.close()
    return "ok", screenshot_path


@celery_app.task()
def snap_images_task(url, timeout=30, proxy=None):  # 默认30秒
    with sync_playwright() as playwright:
        try:
            status, msg = snap_images(playwright, url, timeout, proxy)
            return status, msg
        except Exception as e:
            return "error", "playwright error: {}".format(str(e))
