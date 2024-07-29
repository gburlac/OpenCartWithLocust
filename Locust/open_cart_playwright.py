import re
from playwright.sync_api import Page, expect, sync_playwright

# host = "http://172.23.176.159/opencart/upload/"
host = "https://opencart.abstracta.us"

with sync_playwright() as playwright:
 browser = playwright.chromium.launch(headless=False, slow_mo=500)
 context = browser.new_context()
 page = context.new_page()
 page.goto(host + "/index.php?route=common/home")
 expect(page).to_have_title("Your Store")
 page.screenshot(path="screens/opencart.png")



browser.close()

playwright.stop()