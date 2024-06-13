from locust import User,HttpUser,task,between

class MyUser(HttpUser):

    wait_time=between(1,2)
    #host="http://newtours.demoaut.com"
    #host="https://demo.opencart.com"
    host = "https://opencart.abstracta.us"


    @task
    def launch_URL(self):
        # self.client.get("/mercurycruise.php",name="viewcruise")
        self.client.get("/index.php?route=common/home", name="Home")
        self.wait_time
        self.client.get("/index.php?route=account/login",name="Login into account")
        self.wait_time
        self.client.get("/index.php?route=product/category&path=24", name="Phones&PDAs")
