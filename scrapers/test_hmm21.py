from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)

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

def test_hmm21(BaseCase):
    url = "https://www.hmm21.com/e-service/general/trackNTrace/TrackNTrace.do"

    self.activate_cdp_mode(url)

    self.sleep(1)

    if(self.is_element_present('button[onclick="agreeAllCookies()"]')):
        self.hover_and_click('button[onclick="agreeAllCookies()"]', 'button[onclick="agreeAllCookies()"]')


    #isMobile
    isMobile = False
    if(self.is_element_present('#trackntrace__container-no')):
        isMobile = True

    if(isMobile == False):
        self.sleep(1)
        self.hover_and_click("input[name=\"srchBlNo1\"]", "input[name=\"srchBlNo1\"]")

        self.sleep(1)
        self.type("input[name=\"srchBlNo1\"]", trackNumber)

        self.sleep(1)
        self.hover_and_click("#srchArea > div > div.bt-btn-wrap > button:nth-child(1)", "#srchArea > div > div.bt-btn-wrap > button:nth-child(1)")

        self.wait_for_element("div.tab-inner:nth-child(11)")

        print(sb.get_page_source())
    else:
        self.sleep(1)
        self.hover_and_click("#trackntrace__container-no", "#trackntrace__container-no")

        self.sleep(1)
        self.type("#trackntrace__container-no", "MVDA46358200")

        self.sleep(1)
        self.hover_and_click("button[onclick=\"mobRetrieveTrackNTrace()\"]", "button[onclick=\"mobRetrieveTrackNTrace()\"]")

        self.wait_for_element(".route-area")
        
        print(self.get_page_source())