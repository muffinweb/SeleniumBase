import asyncio
from seleniumbase.core import sb_cdp
from seleniumbase.undetected.cdp_driver import cdp_util

# Start AsyncIO Loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# Set Remote Browser Host and Port
host = "127.0.0.1"
port = 9222

# Initial Driver and Page
driver = loop.run_until_complete(cdp_util.start(host=host, port=port))
page = loop.run_until_complete(driver.get("https://seleniumbase.io/"))

# Create instance to reach cdp methods
sb = sb_cdp.CDPMethods(loop, page, driver)

sb.sleep(2)
print(sb.get_title())
sb.click("CDP Mode")
sb.sleep(2)
print(sb.get_title())

sb.sleep(2)
sb.get("https://www.google.com.tr")

sb.wait_for_element_visible(".gLFyf")
sb.sleep(2)

sb.gui_hover_element(".gLFyf")
print("======== Test Done ========")