from fake_useragent import UserAgent
import asyncio
import time
import sys
import ast
import colorama
import mycdp
from seleniumbase.undetected.cdp_driver import cdp_util
import subprocess
import json

# Fast API
from typing import Union
from fastapi import FastAPI
app = FastAPI()

# Benchmark
import time

# Viewport
import random

# User Agent Explorer
ua = UserAgent(os='Windows')
userAgent = ua.edge

# Yaygın ekran çözünürlükleri (gerçek kullanıcı verilerinden alınmış)
def get_random_resolution():
    # Yaygın ekran çözünürlükleri (gerçek kullanıcı verilerinden alınmış)
    COMMON_RESOLUTIONS = [
        (1920, 1080),
        (1366, 768),
        (1280, 720),
        (1024, 768),
        (1280, 800),
        (1360, 768),
        (800, 600),
    ]

    width, height = random.choice(COMMON_RESOLUTIONS)

    return {"width": width, "height": height}

@app.get("/")
def read_root():
    return {"Hello": "Worlsd"}

@app.get("/ls")
def read_root():
    result = subprocess.run("ls -a", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="cp437")
    output = result.stdout
    return_code = result.returncode
    return {"return_code": return_code, "output": output}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/hyundai/daemon/{trackingNumber}")
async def hyundai_daemon_scrape(trackingNumber: str):
    # If server is windows
    WIN_COMMAND = "docker run -it --rm -v C:/Users/Shipsgo_Ugur/Desktop/seleniumbasedocker/SeleniumBase/scrapers:/SeleniumBase/scrapers:rw seleniumbase python3 carriers/hyundai/hyundai-scrape.py " + str(trackingNumber)

    # server is linux
    LIN_COMMAND = "docker run -it --rm -v /root/srv/seleniumbase/SeleniumBase/scrapers:/SeleniumBase/scrapers:rw seleniumbase python3 carriers/hyundai/hyundai-scrape.py " + str(trackingNumber)

    result = subprocess.run(
        args=LIN_COMMAND,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
        text=True,
        encoding="utf8"
    )

    output = result.stdout
    return_code = result.returncode

    return {"return_code": return_code, "result": output}

@app.get("/hyundai/{trackingNumber}/{chromePort}")
async def hyundai_scrape(trackingNumber: str, chromePort: str):

    xhr_requests = []
    last_xhr_request = None
    c1 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
    c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
    cr = colorama.Style.RESET_ALL
    if "linux" in sys.platform:
        c1 = c2 = cr = ""

    def listenXHR(page):
        async def handler(evt):
            # Get AJAX requests
            if evt.type_ is mycdp.network.ResourceType.XHR:
                xhr_requests.append([evt.response.url, evt.request_id])
                global last_xhr_request
                last_xhr_request = time.time()

        page.add_handler(mycdp.network.ResponseReceived, handler)

    async def receiveXHR(page, requests):
        responses = []
        retries = 0
        max_retries = 5
        # Wait at least 2 seconds after last XHR request for more
        while True:
            if last_xhr_request is None or retries > max_retries:
                break
            if time.time() - last_xhr_request <= 2:
                retries = retries + 1
                time.sleep(2)
                continue
            else:
                break
        await page
        # Loop through gathered requests and get response body
        for request in requests:
            try:
                res = await page.send(mycdp.network.get_response_body(request[1]))
                if res is None:
                    continue
                responses.append({
                    "url": request[0],
                    "body": res[0],
                    "is_base64": res[1],
                })
            except Exception as e:
                print("Error getting response:", e)
        return responses

    async def scrape_tracking_data(trackingNumber: str, chromePort: int):
        page = None
        del page
        host = "127.0.0.1"
        port = chromePort
        driver = await cdp_util.start(host=host, port=port)
        page = await driver.get(url="https://www.hmm21.com/e-service/general/trackNTrace/TrackNTrace.do")

        # page = tab also
        # Listen XHR events
        listenXHR(page)

        start_time = time.time()  # Başlangıç zamanı
        await asyncio.sleep(3)

        blInput = await page.select('input[name="srchBlNo1"]')
        await blInput.mouse_move_async()
        await blInput.mouse_click_async()
        await blInput.send_keys_async(trackingNumber)
        await asyncio.sleep(2)

        retrieveButton = await page.select('#srchArea > div > div.bt-btn-wrap > button:nth-child(1)')
        await retrieveButton.mouse_click_async()

        await page.wait_for("#trackingInfomationDateResultTable > div:nth-child(11) > div.tab-title-wrap > div.tab-title")

        # Get XHR Events
        xhr_responses = await receiveXHR(page, xhr_requests)

        for response in xhr_responses:
            print(c1 + "*** ==> XHR Request URL <== ***" + cr)
            print(f'{response["url"]}')
            is_base64 = response["is_base64"]
            b64_data = "Base64 encoded data"
            try:
                headers = ast.literal_eval(response["body"])["headers"]
                print(c2 + "*** ==> XHR Response Headers <== ***" + cr)
                print(headers if not is_base64 else b64_data)
            except Exception:
                response_body = response["body"]
                print(c2 + "*** ==> XHR Response Body <== ***" + cr)
                print(response_body if not is_base64 else b64_data)

        page_content = await page.get_content()

        # Benchmark
        end_time = time.time()  # Bitiş zamanı
        elapsed_time = end_time - start_time
        benchmark_time = f"Geçen süre: {elapsed_time:.5f} saniye"

        return {
            "benchmark_time": benchmark_time,
            "xhr_responses": xhr_responses,
            "content": page_content
        }

    chromePort = int(chromePort)
    results = await scrape_tracking_data(trackingNumber, chromePort)
    return {"benchmark": results["benchmark_time"], "xhr_responses": results["xhr_responses"], "content": results["content"]}