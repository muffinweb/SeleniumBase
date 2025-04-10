from seleniumbase import SB
from fake_useragent import UserAgent
import proxypicker
import asyncio
import sys

# Proxy explorer
proxyAuth = asyncio.run(proxypicker.get_proxy())
proxy = proxypicker.buildProxyStr(proxyAuth)

# User Agent Explorer
ua = UserAgent(os='Linux')
userAgent = ua.chrome

# TrackNumber
# MVDA46358200
# KHIE90035400
trackNumber = sys.argv[1]


with SB(uc=True, agent=userAgent, proxy=proxy) as sb:
    url = "https://www.hmm21.com/e-service/general/trackNTrace/TrackNTrace.do"

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
        sb.type("input[name=\"srchBlNo1\"]", trackNumber)

        sb.sleep(1)
        sb.hover_and_click("#srchArea > div > div.bt-btn-wrap > button:nth-child(1)", "#srchArea > div > div.bt-btn-wrap > button:nth-child(1)")

        sb.wait_for_element("div.tab-inner:nth-child(11)")

        print(sb.get_page_source())
    else:
        sb.sleep(1)
        sb.hover_and_click("#trackntrace__container-no", "#trackntrace__container-no")

        sb.sleep(1)
        sb.type("#trackntrace__container-no", "MVDA46358200")

        sb.sleep(1)
        sb.hover_and_click("button[onclick=\"mobRetrieveTrackNTrace()\"]", "button[onclick=\"mobRetrieveTrackNTrace()\"]")

        sb.wait_for_element(".route-area")

        print(sb.get_page_source())