from seleniumbase import SB
from fake_useragent import UserAgent

ua = UserAgent(os='Linux')
userAgent = ua.chrome

with SB(uc=True,agent=userAgent,headed=True,xvfb=True) as sb:
    sb.open('https://abrahamjuliot.github.io/creepjs/')
    sb.sleep(3)
    sb.set_window_size(1920, 1080)
    sb.save_screenshot('benchmark_docker.png')
    sb.sleep(2)
    print("Bench Completed")