import time

from seleniumbase import SB

with SB(uc=True,test=True) as sb:
    sb.open('https://abrahamjuliot.github.io/creepjs/')
    time.sleep(5)
    sb.set_window_size(1920, 1080)
    sb.assert_element('#fingerprint-data > div.visitor-info > div > div:nth-child(2) > div:nth-child(2) > span')
    trust_score = sb.get_text('#fingerprint-data > div.visitor-info > div > div:nth-child(2) > div:nth-child(2) > span')
    print("=====================")
    print("   Score: " + str(trust_score))
    print("=====================")
