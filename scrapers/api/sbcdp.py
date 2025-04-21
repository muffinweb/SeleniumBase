import asyncio
from seleniumbase.core import sb_cdp
from seleniumbase.undetected.cdp_driver import cdp_util

## Asenkron döngü başlat
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# Host ve port verilerini gir
host = "127.0.0.1"
port = 9222


driver = loop.run_until_complete(cdp_util.start(host=host, port=port, window))
page = loop.run_until_complete(driver.get("https://seleniumbase.io/"))
sb = sb_cdp.CDPMethods(loop, page, driver)
sb.sleep(2)
print(sb.get_title())
sb.gui_click_element(".md-ellipsis")
sb.sleep(2)
print(sb.get_title())