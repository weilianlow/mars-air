from playwright.sync_api import Page


class Home:
    def __init__(self, page: Page):
        self.page = page
        self.departing_select = page.locator('//select[@id="departing"]')
        self.returning_select = page.locator('//select[@id="returning"]')
        self.promo_code_text = page.locator('//input[@id="promotional_code"]')
        self.search_button = page.locator('//input[@value="Search"]')
        self.back_link = page.locator('//a[contains(text(),"Back")]')
        self.search_title = page.locator('//div[@id="content"]/h2')
        self.form_content = page.locator('//div[@id="content"]/p')

    def navigate(self):
        self.page.goto("https://marsair.recruiting.thoughtworks.net/WeiLianLow")

    def search(self, departing=None, returning=None, promo_code=None):
        if departing:
            self.departing_select.select_option(departing)
        if returning:
            self.returning_select.select_option(returning)
        if promo_code:
            self.promo_code_text.fill(promo_code)
        self.search_button.click()
