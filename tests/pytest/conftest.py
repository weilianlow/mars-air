import pytest
from requests import Session
from playwright.sync_api import Playwright


@pytest.fixture(scope='module')
def chrome(playwright: Playwright):
    browser = None
    try:
        chromium = playwright.chromium
        browser = chromium.launch()
        yield browser
    finally:
        if browser:
            browser.close()


@pytest.fixture(autouse=True, scope='module')
def session():
    s = None
    try:
        url = 'https://marsair.recruiting.thoughtworks.net/WeiLianLow'
        s = Session()
        s.headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
        yield s, url
    finally:
        if s:
            s.close()
