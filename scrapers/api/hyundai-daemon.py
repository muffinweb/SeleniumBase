import asyncio
import sys
import ast
import colorama
import mycdp
from seleniumbase.undetected.cdp_driver import cdp_util

# Benchmark
import time

async def hyundai_scrape():
    xhr_requests = []
    last_xhr_request = None
    c1 = colorama.Fore.BLUE + colorama.Back.LIGHTYELLOW_EX
    c2 = colorama.Fore.BLUE + colorama.Back.LIGHTGREEN_EX
    cr = colorama.Style.RESET_ALL
    #if "linux" in sys.platform:
    #    c1 = c2 = cr = ""

    async def listenXHR(page):
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

    host = "0.0.0.0"
    port = 9222
    driver = await cdp_util.start(host=host, port=port)
    page = await driver.get("https://www.hmm21.com/e-service/general/trackNTrace/TrackNTrace.do")
    await listenXHR(page.browser.main_tab)

    # wait for element to be existed
    await page.wait_for('input[name="srchBlNo1"]')



    start_time = time.time()  # Başlangıç zamanı

    blInput = await page.select('input[name="srchBlNo1"]', 20)
    await blInput.mouse_move_async()
    await blInput.mouse_click_async()
    await blInput.send_keys_async("NBOZ23602900")
    await asyncio.sleep(2)

    retrieveButton = await page.select('#srchArea > div > div.bt-btn-wrap > button:nth-child(1)')
    await retrieveButton.mouse_click_async()

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

    results = {
        "benchmark_time": benchmark_time,
        "xhr_responses": xhr_responses,
        "content": page_content
    }

    return {"benchmark": results["benchmark_time"], "xhr_responses": results["xhr_responses"],
            "content": results["content"]}

print(asyncio.run(hyundai_scrape()))
