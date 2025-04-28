import sys
import ast
import mycdp
import asyncio
import colorama
import proxypicker
from seleniumbase import SB
from fake_useragent import UserAgent

# Benchmark
import time

# Randomizer for picking Viewport
import random


# Yaygın viewportlar
def get_random_resolution():
    # Yaygın ekran çözünürlükleri (gerçek kullanıcı verilerinden alınmış)
    COMMON_RESOLUTIONS = [
        (1920, 1080),
        (1366, 768),
         (1280, 720),
        # (1024, 768),
        # (1280, 800),
        # (1360, 768),
        # (800, 600),
    ]

    width, height = random.choice(COMMON_RESOLUTIONS)

    return str(width) + "," + str(height)


viewport = get_random_resolution()

# TrackNumber
# MVDA46358200
# KHIE90035400
trackNumber = sys.argv[1]

# Proxy explorer
proxyAuth = asyncio.run(proxypicker.get_proxy())
proxy = proxypicker.buildProxyStr(proxyAuth)

# Get Random OS

# User Agent Explorer
ua = UserAgent(os='Windows')
userAgent = ua.chrome

with SB(uc=True, agent=userAgent, incognito=True, window_size=viewport) as sb:

    xhr_requests = []
    last_xhr_request = None
    c1 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
    c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
    cr = colorama.Style.RESET_ALL

    # if "linux" in sys.platform:
    #    c1 = c2 = cr = ""

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

    sb.activate_cdp_mode("about:blank")
    tab = sb.cdp.page

    # Listen XHR on related tab
    listenXHR(tab)

    # Website to scrape
    url = "https://myturkonline.turkon.com/tracking"

    # Change url to something that makes ajax requests
    sb.cdp.open(url)

    time.sleep(2)

    sb.uc_gui_click_captcha()

    sb.wait_for_ready_state_complete()

    # Benchmark START
    start_time = time.time()  # Başlangıç zamanı

    ### Browser Automation Actions - START ###

    # Sayfanin yuklenmesini bekle
    sb.wait_for_ready_state_complete()

    # Submit butonunun varligini dogrula
    sb.wait_for_element('button[type="submit"]')

    # Inputa degeri gir
    sb.type('input', trackNumber)

    # sorgulamayi baslat
    sb.uc_click('button[type="submit"]')

    # Cevabin döndüğünü doğrula
    sb.wait_for_text(text="Yükleme Bilgileri", selector="app-layout")

    ### Browser Automation Actions - END ###

    time.sleep(2)

    # Getting XHR logs
    loop = sb.cdp.get_event_loop()
    xhr_responses = loop.run_until_complete(receiveXHR(tab, xhr_requests))
    for response in xhr_responses:
        #print(c1 + "*** ==> XHR Request URL <== ***" + cr)
        #print(f'{response["url"]}')
        is_base64 = response["is_base64"]
        b64_data = "Base64 encoded data"
        try:
            headers = ast.literal_eval(response["body"])["headers"]
            #print(c2 + "*** ==> XHR Response Headers <== ***" + cr)
            #print(headers if not is_base64 else b64_data)
        except Exception:
            response_body = response["body"]
            #print(c2 + "*** ==> XHR Response Body <== ***" + cr)
            #print(response_body if not is_base64 else b64_data)

    # Benchmark END
    end_time = time.time()  # Bitiş zamanı
    elapsed_time = end_time - start_time
    benchmark_time = f"Geçen süre: {elapsed_time:.5f} saniye"

    print({"benchmark": benchmark_time, "xhr_responses": xhr_responses, "output": sb.get_page_source()})