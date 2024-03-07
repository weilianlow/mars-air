import unittest
from playwright.sync_api import sync_playwright

from tests.models.home import Home


class Case(unittest.TestCase):
    browser = None

    @classmethod
    def setUpClass(cls):
        try:
            playwright = sync_playwright().start()
            chromium = playwright.chromium
            cls.browser = chromium.launch()
        except:
            if cls.browser:
                cls.browser.close()


class TestReturnToHome(Case):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        page = self.browser.new_page()
        self.home = Home(page)
        self.home.navigate()

    def test_return_to_home_via_back_hyperlink(self):
        self.home.search("July", "December (two years from now)", None)
        assert self.home.search_title.text_content() == "Search Results"
        self.home.back_link.click()
        assert self.home.search_title.text_content() == "Welcome to MarsAir!"

    def test_return_to_home_via_home_hyperlink(self):
        self.home.search("July", "December (two years from now)", None)
        assert self.home.search_title.text_content() == "Search Results"
        self.home.home_link.click()
        assert self.home.search_title.text_content() == "Welcome to MarsAir!"
