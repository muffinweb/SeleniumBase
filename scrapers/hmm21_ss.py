from seleniumbase import SB
from fake_useragent import UserAgent

ua = UserAgent(os='Linux')
userAgent = ua.chrome

with SB(uc=True,agent=userAgent,headed=True,xvfb=True) as sb:
    sb.open('https://www.hmm21.com/e-service/general/trackNTrace/TrackNTrace.do')
    sb.sleep(3)
    sb.set_window_size(1920, 1080)
    sb.save_screenshot('hmm21_screenshot.png')
    sb.sleep(10)
    print("Bench Completed")