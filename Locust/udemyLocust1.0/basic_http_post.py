from locust import HttpUser,task,between

class MyUser(HttpUser):

    wait_time=between(1,2)
    #host="http://newtours.demoaut.com"
    host = "https://opencart.abstracta.us"

    @task
    def launch_URL(self):
        self.client.get("/index.php?route=account/login",name="Login into account")

    @task
    def login(self):
        #self.client.post("/login.php",name="login",data={"action": "process","userName": "qamile1@gmail.com","password": "qamile","login.x": "41","login.y": "12"})
        self.client.post("/index.php?route=account/login",name="login",data={"email": "JBoo@gmail.com","password": "parola12"})
