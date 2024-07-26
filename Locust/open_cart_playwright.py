import re
from playwright.sync_api import Page, expect, sync_playwright

playwright = sync_playwright().start()
browser = playwright.chromium.launch(headless=False)
page = browser.new_page()
page.goto("http://172.23.176.159/opencart/upload/index.php?route=common/home")
expect(page).to_have_title("Your Store")
page.screenshot(path="screens/opencart.png")
browser.close()

playwright.stop()