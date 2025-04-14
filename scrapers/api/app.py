# Seleniumbase
from seleniumbase import SB
from fake_useragent import UserAgent
import proxypicker
import asyncio
import sys

# Fast API
from typing import Union
from fastapi import FastAPI
app = FastAPI()

# Benchmark
import time

# Viewport
import random

# Proxy explorer
proxyAuth = asyncio.run(proxypicker.get_proxy())
proxy = proxypicker.buildProxyStr(proxyAuth)

# User Agent Explorer
ua = UserAgent(os='Microsoft')
userAgent = ua.edge

# Yaygın ekran çözünürlükleri (gerçek kullanıcı verilerinden alınmış)
def get_random_resolution():
    # Yaygın ekran çözünürlükleri (gerçek kullanıcı verilerinden alınmış)
    COMMON_RESOLUTIONS = [
        (1920, 1080),
        (1366, 768),
        (1440, 900),
        (1536, 864),
        (1280, 720),
        (1600, 900),
        (1024, 768),
        (2560, 1440),
        (1280, 800),
        (1360, 768),
        (800, 600),
    ]

    width, height = random.choice(COMMON_RESOLUTIONS)

    return {"width": width, "height": height}

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/scrape/hyundai/{tracknumber}/{anothertrucknumber}")
def hyundai(tracknumber: str):
    
    start_time = time.time()  # Başlangıç zamanı

    try:
        with SB(uc=True, agent=userAgent, proxy=proxy,test=True,xvfb=True,headed=True) as sb:

            url = "https://www.hmm21.com/e-service/general/trackNTrace/TrackNTrace.do"

            resolution = get_random_resolution()
            sb.set_window_size(resolution["width"], resolution["height"])

            sb.activate_cdp_mode(url)

            sb.sleep(1)

            if(sb.is_element_present('button[onclick="agreeAllCookies()"]')):
                sb.hover_and_click('button[onclick="agreeAllCookies()"]', 'button[onclick="agreeAllCookies()"]')

            #isMobile
            isMobile = False
            if(sb.is_element_present('#trackntrace__container-no')):
                isMobile = True

            if(isMobile == False):
                sb.sleep(1)
                sb.hover_and_click("input[name=\"srchBlNo1\"]", "input[name=\"srchBlNo1\"]")

                sb.sleep(1)
                sb.type("input[name=\"srchBlNo1\"]", tracknumber)

                sb.sleep(1)
                sb.hover_and_click("#srchArea > div > div.bt-btn-wrap > button:nth-child(1)", "#srchArea > div > div.bt-btn-wrap > button:nth-child(1)")

                sb.wait_for_element("div.tab-inner:nth-child(11)")

                response = sb.get_page_source()

                end_time = time.time()  # Bitiş zamanı
                elapsed_time = end_time - start_time
                benchmark_time = f"Geçen süre: {elapsed_time:.5f} saniye"
                return {"isResponsiveUI": True, "benchTime": benchmark_time, "content": response}
            else:
                sb.sleep(2)
                sb.hover_and_click("#trackntrace__container-no", "#trackntrace__container-no")

                sb.sleep(2)
                sb.type("#trackntrace__container-no", "MVDA46358200")

                sb.sleep(2)
                sb.hover_and_click("button[onclick=\"mobRetrieveTrackNTrace()\"]", "button[onclick=\"mobRetrieveTrackNTrace()\"]")

                sb.wait_for_element(".route-area")

                response = sb.get_page_source()

                end_time = time.time()  # Bitiş zamanı
                elapsed_time = end_time - start_time
                benchmark_time = f"Geçen süre: {elapsed_time:.5f} saniye"
                return {"isResponsiveUI": False, "benchTime": benchmark_time, "content": response}
    except Exception as error:
        return {"error": error}
    