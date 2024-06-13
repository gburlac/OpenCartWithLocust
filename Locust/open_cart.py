import random
import open_cart_login_reader
from locust import task, between, SequentialTaskSet, FastHttpUser
from bs4 import BeautifulSoup


class OpenCart(SequentialTaskSet):

    @task()
    def launcher(self):
        with self.client.get("/index.php?route=common/home", name="Home", catch_response=True) as resp1:
            #print("resp1"+ resp1.text)
            #resp1.cookies['OCSESSID']
            #session_id = resp1
            #print("Session = "+ session_id)
            resp1.success("204")
            if ("Featured") in resp1.text:
                resp1.success()
            else:resp1.failure("failed to load")

    @task
    def login_account(self):
        csvLogin = open_cart_login_reader()
        #customer = next(csvUsers)
        #with self.client.post("/index.php?route=account/login",name="Login_account",data={"email": customer[0],"password": customer[1]}, catch_response=True) as resp2:
        with self.client.post("/index.php?route=account/login",name="Login_account",data={"email": "JBoo@gmail.com","password":"parola12"}, catch_response=True) as resp2:
         #print("Response" +resp2.text)
         resp2.success("204")
         if ("Your Store") in resp2.text:
            resp2.success()
         else:
            resp2.failure("failed")

    @task
    def access_category(self):
      with  self.client.get("/index.php?route=product/category&path=24", name="Category", catch_response=True) as resp3:
        if("Your Store") in resp3.text:
            resp3.success()
        else:
            resp3.failure("failed")
    @task
    def select_product(self):
     with  self.client.get("/index.php?route=product/product&path=24", name="Select_product", catch_response=True) as resp4:
         soup = BeautifulSoup(resp4.content, 'html.parser')
         product_id_list = soup.find_all('h4')
         patern = "product_id=(\d*)"
         random_product_id = random.sample(product_id_list, 1)
         random_product_id1 = re.findall(patern, str(random_product_id))[0]

     if ("Reviews") not in resp4.text:
            resp4.failure("failed")
     else:
            resp4.success()

    @task
    def add_wishlist(self):
     with self.client.post("/index.php?route=account/wishlist/add", name="Add_wishlist", data={"product_id":"1"}, catch_response=True) as resp5:
        if("Success: You have added") in resp5.text:
            resp5.success()
        else:
            resp5.failure("failed")
    @task
    def add_cart(self, random_product_id1):
     with self.client.post("/index.php?route=checkout/cart/add", name="Add_cart",data={"quantity": "1", "product_id": random_product_id1}, catch_response=True) as resp6:
         #print("resp6 " + resp6)
         if("Total") in resp6.text:
             resp6.success()
         else:
             resp6.failure("failed")

class Runner(FastHttpUser):
    wait_time = between(1, 4)
    host = "https://opencart.abstracta.us"
    tasks = [OpenCart]