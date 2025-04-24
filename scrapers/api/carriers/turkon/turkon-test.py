import sys
from seleniumbase import SB

# An bad UserAgent forces CAPTCHA-solving on macOS
agent = "cool"
if "linux" in sys.platform or "win32" in sys.platform:
    agent = None  # Use the default UserAgent

with SB(uc=True, test=True, rtf=True, agent=agent, incognito=True) as sb:
    url = "https://myturkonline.turkon.com/tracking"
    sb.uc_open_with_reconnect(url)
    sb.uc_gui_click_captcha()  # Only if needed
    sb.assert_title("My Turkon")