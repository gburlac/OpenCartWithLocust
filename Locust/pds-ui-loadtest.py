from locust import between, FastHttpUser, SequentialTaskSet
from locust.user import task


class PDSUILoadtest(SequentialTaskSet):
    @task
    def launcher(self):
        with self.client.get("/auth/realms/crossproduct/login-actions/authenticate?execution=aeba59ec-5bad-4499-9b37-2ac9161c7cfc&client_id=saml&tab_id=z1OWTFRLs7M", name="Login") as resp1:
            print("resp1===  " + resp1.text)




class Runner(FastHttpUser):
    wait_time = between(1, 4)
    host = "https://ui1.ft1-core.mpp:8443"
    tasks = [PDSUILoadtest]