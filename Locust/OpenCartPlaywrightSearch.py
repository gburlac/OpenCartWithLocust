import logging
import random
import re
from playwright.sync_api import Playwright, sync_playwright, expect
from csvreader import CSVReader

# host = "http://172.23.176.159/opencart/upload/"
host = "https://opencart.abstracta.us"


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False, slow_mo=900)
    context = browser.new_context()
    page = context.new_page()

    #Home-page
    page.goto(host)
    print("Accessing Home page for host " + host)
    expect(page).to_have_title("Your Store")
    page.screenshot(path="screens/opencartHome.png", full_page=True)

    #Login
    page.get_by_role("link", name=" My Account").click()
    page.get_by_role("link", name="Login").click()
    my_reader = CSVReader("C:\\projects\\OpenCartWithLocust\\Locust\\users.csv").read_data()
    # username = my_reader.pop()['username']
    # password = my_reader.pop()['password']
    username = random.choice(my_reader)['username']
    password = random.choice(my_reader)['password']
    page.get_by_placeholder("E-Mail Address").click()
    page.get_by_placeholder("E-Mail Address").fill(username)
    page.get_by_placeholder("Password").click()
    page.get_by_placeholder("Password").fill(password)
    page.get_by_role("button", name="Login").click()
    print("Logining with user: " + username)
    expect(page).to_have_title("My Account")
    page.screenshot(path="screens/opencartLogin.png", full_page=True)

    #Search
    product_reader = CSVReader("C:\\projects\\OpenCartWithLocust\\Locust\\product.csv").read_data()
    product = random.choice(product_reader)['product']
    page.get_by_placeholder("Search").click()
    page.get_by_placeholder("Search").fill(product)
    page.get_by_role("button", name="").click()
    page.get_by_role("link", name= product).first.click()
    print("Searching for product: " + product)
    expect(page).to_have_title(product)
    page.screenshot(path="screens/opencarSearch.png", full_page=True)

    #Add to Cart
    page.get_by_role("button", name="Add to Cart", exact=True).click()
    print("Adding to cart product: " + product)

    #Go to Cart
    page.get_by_role("link", name="shopping cart", exact=True).click()
    print("Going to cart to view product: " + product)
    expect(page.locator("#checkout-cart")).to_contain_text("Shopping Cart")
    page.screenshot(path="screens/opencartViewCart.png", full_page=True)

    #Logout
    page.get_by_role("link", name=" My Account").click()
    page.get_by_role("link", name="Logout").click()
    print("Logining out from host " + host)
    expect(page.locator("#content")).to_contain_text(
        "You have been logged off your account. It is now safe to leave the computer.")
    page.screenshot(path="screens/opencartLogOut.png", full_page=True)
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
