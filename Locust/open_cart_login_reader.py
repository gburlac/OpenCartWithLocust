from locust import User, constant
import csv

USER_CREDENTIALS = []


class open_cart_login_reader(User):
    username = "NOT_FOUND"
    password = "NOT_FOUND"

    def readCredsFromCSV(self):
        global USER_CREDENTIALS
        with open('users.csv', 'r') as f:
            reader = csv.reader(f)
            USER_CREDENTIALS = list(reader)
            return USER_CREDENTIALS

    def useEachCredPairOnlyOnce(self):
        if len(USER_CREDENTIALS) > 0:
            self.username, self.password = USER_CREDENTIALS.pop()

    tasks = [readCredsFromCSV]
    wait_time = constant(1)
