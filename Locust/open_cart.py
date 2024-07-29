import logging
import random
import re

from bs4 import BeautifulSoup
from locust import task, between, SequentialTaskSet, FastHttpUser, HttpUser

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
        #self.username = random.choice(my_reader)['username']
        self.username = my_reader.pop()['username']
        self.password = my_reader.pop()['password']
        #print("Random username=== " + self.username)
        with self.client.post("/index.php?route=account/login",
                              name="Login to account",
                              data={"email": self.username, "password": self.password},
                              catch_response=True) as resp2:
            # print("Response" +resp2.text)
            if "Your Store" in resp2.text:
                resp2.success()
            else:
                resp2.failure("failed")
        #soup = BeautifulSoup(resp2.content, 'html.parser')
        #path_id_list = soup.find_all('h5')
        #patern = "path=(\d*)"
        #random_path_tags = random.sample(path_id_list, 1)
        #randPathTag = random_path_tags[0]
        #self.random_path_id = re.findall(patern, str(randPathTag))[0]
        #print("Random category=== " + self.random_path_id)
        logging.info('Logining into the site with username \t'+self.username+ '...')

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
        self.random_product_id = re.findall('product_id=\d*', str(random.sample(soup.find_all('h4'), 1)))[0]
        print("Random product_id=== " + self.random_product_id)
        logging.info('Accessing a category...')

    @task()
    def select_product(self):
        with  self.client.get("/index.php?route=product/category&path=24&product_id="+self.random_product_id,
                              name="Select product",
                              catch_response=True) as resp4:
            # print("Response=== " +resp4.text)
            if "Your Store" in resp4.text:
                resp4.success()
            else:
                resp4.failure("failed")
        logging.info(f'Select a random product with id...  {self.random_product_id} ...')

    @task()
    def add_wishlist(self):
        with self.client.post(f"/index.php?route=account/wishlist/add", {"product_id":{self.random_product_id}},
                              name="Add to wishlist",
                              catch_response=True) as resp5:
            #print("Response5=== " + resp5.text)
            if "Success: You have added" and "wish list" in resp5.text:
                resp5.success("Passed")
            else:
                resp5.failure("Failed")
        logging.info('Product %s has been added to wishlist...', self.random_product_id)

    @task()
    def add_cart(self):
        with self.client.post(f"/index.php?route=checkout/cart/add", {"quantity": "1", "product_id": {self.random_product_id}},
                              name="Add to cart",
                              catch_response=True) as resp6:
          #print("Response6=== " + resp6.text)
         if " Success: You have added " and "to your shoppingcart! " in resp6.text:
            resp6.success("Passed")
         else:
            resp6.failure("Failed")

        with self.client.get("/index.php?route=checkout/cart",
                             name="Verify cart ",
                             catch_response=True) as resp7:
            #print("Response7=== " + resp7.text)
            if "Shopping Cart" in resp7.text:
                resp7.success("Passed")
            else:
                resp7.failure("Failed")
            logging.info('Product %s has been added', self.random_product_id)

class Runner(FastHttpUser):
    wait_time = between(1, 4)
    #host = "http://172.23.176.159/opencart/upload/"
    host = "https://opencart.abstracta.us"
    tasks = [OpenCart]
