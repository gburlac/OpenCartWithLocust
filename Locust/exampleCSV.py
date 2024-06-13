import random

from csvreader import CSVReader

my_reader = CSVReader("C:\\projects\\OpenCartWithLocust\\Locust\\users.csv").read_data()

#print(my_reader)

username = my_reader.pop()['username']
username0 = random.choice( my_reader)['username']
username1 = my_reader.pop(1)

print(username0)

