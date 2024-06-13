from locust import User,task,between

class MyUser(User):

    wait_time=between(1,2)

    @task(2)
    def add_cart(self):
     print("I am add to cart")

    @task(3)
    def view_product(self):
     print("I am view product")

     @task(4)
     def log_out(self):
         print("Leaving the site")