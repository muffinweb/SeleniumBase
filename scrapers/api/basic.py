from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)

class MyTestClass(BaseCase):
    def test_demo_site(self):
        self.open("https://seleniumbase.io/demo_page")
        self.type("#myTextInput", "This is Automated")
        self.click("#myButton")
        self.assert_element("tbody#tbodyId")
        self.assert_text("Automation Practice", "h3")
        self.click_link("SeleniumBase Demo Page")
        self.assert_exact_text("Demo Page", "h1")
        self.assert_no_js_errors()