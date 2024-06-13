# thislist = ["apple", "banana", "cherry"]
# for x in thislist:
#   print(x)
#   thislist.sort()
#   print(thislist)
import random


def digitize(n):
    return [int(y) for y in str(n)[::-1]]
n = 4321
reversed = digitize(n)
print(reversed)

def cuvint(c):
  return c
c = "BMW X3"
str = cuvint(c)
print(str)

def range_between(a,b):
    return list(range(a,b + 1))
a = 1
b = 9
between = range_between(a,b)
print(between)

def random_num(c, d):
    return random.randrange(c, d)
c = 10000001
d = 99999990
random_num_between = random_num(c,d)
print(random_num_between)