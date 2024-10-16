def task_1():
  inch = float(input())

  print("cm: " + str(inch * 2.54))

def task_2():
  name = input()

  print("Hello, " + name + "!")

def task_3():
  first_name = input("First name:")
  last_name = input("Last name:")
  age = int(input("Age:"))
  city = input("City:")

  print(f"You are {first_name} {last_name}, a {age}-years old person from {city}.")
