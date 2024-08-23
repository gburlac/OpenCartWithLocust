import logging
import random
import re

import self
from bs4 import BeautifulSoup
from locust import task, between, SequentialTaskSet, FastHttpUser, events

from csvreader import CSVReader


class OpenCart(SequentialTaskSet):

    @task()
    def launching_home_page(self):
        with self.client.get("/index.php?route=common/home", name="Home", catch_response=True) as resp1:
            # print("resp1 "+ resp1.text)
            # resp1.cookies['OCSESSID']
            # session_id = resp1
            # print("Session = "+ session_id)
            if "Featured" in resp1.text:
                resp1.success()
            else:
                resp1.failure("failed to load")
        logging.info('Accesing Home page...')

    @task()
    def login_account(self):
        my_reader = CSVReader("C:\\projects\\OpenCartWithLocust\\Locust\\users.csv").read_data()
        username = random.choice(my_reader)['username']
        password = random.choice(my_reader)['password']
        # self.username = my_reader.pop()['username']
        # self.password = my_reader.pop()['password']
        # print("Random username=== " + self.username)
        with self.client.post("/index.php?route=account/login",
                              name="Login to account",
                              data={"email": username, "password": password},
                              catch_response=True) as resp2:
            # print("Response" +resp2.text)
            if "Your Store" in resp2.text:
                resp2.success()
            else:
                resp2.failure("failed")
        # soup = BeautifulSoup(resp2.content, 'html.parser')
        # path_id_list = soup.find_all('h5')
        # patern = "path=(\d*)"
        # random_path_tags = random.sample(path_id_list, 1)
        # randPathTag = random_path_tags[0]
        # self.random_path_id = re.findall(patern, str(randPathTag))[0]
        # print("Random category=== " + self.random_path_id)
        logging.info('Logining into the site with username: ' + username + '...')

    @task()
    def access_category(self):
        with  self.client.get("/index.php?route=product/category&path=24",
                              name="Access a Category",
                              catch_response=True) as resp3:
            if "Your Store" in resp3.text:
                resp3.success()
            else:
                resp3.failure("failed")
        soup = BeautifulSoup(resp3.content, 'html.parser')
        self.random_product_id = re.findall("product_id=(\d*)", str(random.sample(soup.find_all('h4'), 1)))[0]
        print(f"Random product_id=== {self.random_product_id}")
        logging.info('Accessing a category...')

    @task()
    def select_product(self):
        with  self.client.get(f'/index.php?route=product/category&path=24&product_id={self.random_product_id}',
                              name="Select product",
                              catch_response=True) as resp4:
            # print("Response=== " +resp4.text)
            if "Your Store" in resp4.text:
                resp4.success()
            else:
                resp4.failure("failed")
        logging.info(f'Select a random product with id...  {self.random_product_id} ...')

    @task()
    def add_cart(self):
        self.rand_quantity = random.randint(1, 9)
        with self.client.post("/index.php?route=checkout/cart/add",
                              name="Add to cart",
                              data={"quantity": "1", "product_id": f"{self.random_product_id}"},
                              catch_response=True) as resp6:
            print("Response6=== " + resp6.text)
            if "You have added" in resp6.text:
                resp6.success("Passed")
            else:
                resp6.failure("Failed")
            logging.info(f"Adding to cart product with id: {self.random_product_id}")

    @task()
    def check_cart(self):
        with self.client.get("/index.php?route=checkout/cart",
                             name="Verify cart ",
                             catch_response=True) as resp7:
            #print("Response7=== " + resp7.text)
            if "What would you like to do next?" in resp7.text:
                resp7.success("Passed")
            else:
                resp7.failure("Failed")
            logging.info(f'Product {self.random_product_id} has been added')


class Runner(FastHttpUser):
    wait_time = between(1, 2)
    # host = "http://172.23.176.159/opencart/upload/"
    host = "https://opencart.abstracta.us"
    tasks = [OpenCart]
