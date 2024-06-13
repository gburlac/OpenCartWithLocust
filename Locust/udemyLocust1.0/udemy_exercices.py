user_num = int(input("Please enter a number: "))

if user_num < 0:
    print("Numer is negative...")
elif user_num == 0:
    print(" number = 0 ")
elif 0 < user_num <= 100:
    print("Number are to 100...")
else:
    print("Number out of range...")

print(bool(0))