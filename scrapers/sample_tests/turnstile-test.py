from seleniumbase import SB

with SB(uc=True, test=True) as sb:
    sb.uc_open_with_reconnect('https://2captcha.com/demo/cloudflare-turnstile')
    sb.uc_gui_click_captcha()