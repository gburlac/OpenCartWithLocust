import random
import re

from bs4 import BeautifulSoup
from locust import task, between, SequentialTaskSet, FastHttpUser

from csvreader import CSVReader


class OpenCart(SequentialTaskSet):

    @task()
    def launcher(self):
        with self.client.get("/index.php?route=common/home", name="Home", catch_response=True) as resp1:
            # print("resp1 "+ resp1.text)
            # resp1.cookies['OCSESSID']
            # session_id = resp1
            # print("Session = "+ session_id)
            if "Featured" in resp1.text:
                resp1.success()
            else:
                resp1.failure("failed to load")

    @task()
    def login_account(self):
        my_reader = CSVReader("C:\\projects\\OpenCartWithLocust\\Locust\\users.csv").read_data()
        self.username = random.choice(my_reader)['username']
        self.password = random.choice(my_reader)['password']
        print("Random username=== "+self.username)
        with self.client.post("/index.php?route=account/login", name="Login to account",
                              data={"email": self.username, "password": self.password}, catch_response=True) as resp2:
            # print("Response" +resp2.text)
            if "Your Store" in resp2.text:
                resp2.success()
            else:
                resp2.failure("failed")

    @task()
    def access_category(self):
        with  self.client.get("/index.php?route=product/category&path=24", name="Access a Category",
                              catch_response=True) as resp3:
            if "Your Store" in resp3.text:
                resp3.success()
            else:
                resp3.failure("failed")
        soup = BeautifulSoup(resp3.content, 'html.parser')
        product_id_list = soup.find_all('h4')
        patern = "product_id=(\d*)"
        random_tags = random.sample(product_id_list, 1)
        randTag = random_tags[0]
        self.random_product_id = re.findall(patern, str(randTag))[0]
        print("Random product_id===" + self.random_product_id)

    @task()
    def select_product(self):
        with  self.client.get("/index.php?route=product/category&path=24&product_id=" +self.random_product_id,
                              name="Select product",
                              catch_response=True) as resp4:
            #print("Response=== " +resp4.text)
            if "Your Store" in resp4.text:
                resp4.success()
            else:
                resp4.failure("failed")

    #@task()
    def add_wishlist(self):
        with self.client.post("/index.php?route=account/wishlist/add", name="Add wishlist", data={"product_id": "1"},
                              catch_response=True) as resp5:
            print("Response5=== " + resp5.text)
            if "wishlist.add" in resp5.text:
                resp5.success()
            else:
                resp5.failure("failed")


    @task()
    def add_cart(self):
        with self.client.post("/index.php?route=checkout/cart/add", name="Add 2 cart",
                              data={"quantity": "1", "product_id": "1"}, catch_response=True) as resp6:
            print("Response6=== " +resp6.text)
            if "Your Store" in resp6.text:
                resp6.success()
            else:
                resp6.failure("failed")

        with self.client.get("/index.php?route=checkout/cart", name="Go 2 cart ", catch_response=True) as resp7:
            print("Response7=== " +resp7.text)
            if "Shopping Cart" in resp7.text:
                resp7.success()
            else:
                resp7.failure("failed")





class Runner(FastHttpUser):
    wait_time = between(1, 4)
    host = "https://opencart.abstracta.us"
    tasks = [OpenCart]
