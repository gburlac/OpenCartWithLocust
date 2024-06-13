import random
import re

from bs4 import BeautifulSoup
from locust import between, FastHttpUser, SequentialTaskSet, task


class OpenCartId(SequentialTaskSet):
   @task()
   def select_product(self):
       response = self.client.get("/index.php?route=product/category&path=24", name="Acces Category")
       soup = BeautifulSoup(response.content, 'html.parser')
       product_id_list = soup.find_all('h4')
       patern = "product_id=(\d*)"
       random_tags = random.sample(product_id_list, 1)
       randTag = random_tags[0]
       self.random_product_id = re.findall(patern, str(randTag))[0]
       print(self.random_product_id)

       with  self.client.get("/index.php?route=product/category&path=24&product_id=" + self.random_product_id, name="Select_product",
                          catch_response=True) as resp4:
           if ("Reviews") not in resp4.text:
               resp4.failure("failed")
           else:
               resp4.success()


class Runner(FastHttpUser):
 wait_time = between(1, 4)
 host = "https://opencart.abstracta.us"
 tasks = [OpenCartId]