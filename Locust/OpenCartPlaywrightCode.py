import random
import re

import self
from playwright.sync_api import Playwright, sync_playwright, expect
from csvreader import CSVReader

# host = "http://172.23.176.159/opencart/upload/"
host = "https://opencart.abstracta.us"
def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False, slow_mo=900)
    context = browser.new_context()
    page = context.new_page()
    #Home Page
    page.goto(host)
    expect(page.locator("#top-links")).to_contain_text("My Account")
    page.screenshot(path="screens/opencartHome.png", full_page=True)

    #Login
    page.get_by_role("link", name=" My Account").click()
    page.get_by_role("link", name="Login").click()
    expect(page.locator("#content")).to_contain_text("Returning Customer")
    my_reader = CSVReader("C:\\projects\\OpenCartWithLocust\\Locust\\users.csv").read_data()
    #username = my_reader.pop()['username']
    #password = my_reader.pop()['password']
    username = random.choice(my_reader)['username']
    password = random.choice(my_reader)['password']
    page.get_by_placeholder("E-Mail Address").click()
    page.get_by_placeholder("E-Mail Address").fill(username)
    page.get_by_placeholder("Password").click()
    page.get_by_placeholder("Password").fill(password)
    page.get_by_role("button", name="Login").click()
    expect(page.locator("h1")).to_contain_text("Your Store")
    page.screenshot(path="screens/opencartLogin.png", full_page=True)

    #Category
    page.get_by_role("link", name="Phones & PDAs").click()
    expect(page.locator("h2")).to_contain_text("Phones & PDAs")
    page.screenshot(path="screens/opencartCategory.png", full_page=True)

    #Product
    page.get_by_role("heading", name="iPhone").get_by_role("link").click()
    expect(page.locator("#button-cart")).to_contain_text("Add to Cart")
    page.screenshot(path="screens/opencartProduct.png", full_page=True)

    #Add to cart
    page.get_by_role("button", name="Add to Cart", exact=True).click()

    #View cart
    page.get_by_role("link", name="shopping cart", exact=True).click()
    expect(page.locator("#checkout-cart")).to_contain_text("Shopping Cart")
    page.screenshot(path="screens/opencartViewCart.png", full_page=True)

    #Log out
    page.get_by_role("link", name=" My Account").click()
    page.get_by_role("link", name="Logout").click()
    expect(page.locator("#content")).to_contain_text("You have been logged off your account. It is now safe to leave the computer.")
    page.screenshot(path="screens/opencartLogOut.png", full_page=True)

    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
