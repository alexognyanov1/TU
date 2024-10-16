# n = int(input("n:"))

# numbers = []
# for i in range(1, n+1):
#   numbers.append(int((input("number:"))))

# print(max(numbers))
# print(sum(numbers))

# for i in range(n, 0, -1):
#   print("* " * i)

numbers = []
moreThan10 = 0

for i in range(10):
  user_input = input("number:")

  if user_input == "":
    print("Invalid input")
    continue
  
  if user_input == "q":
    break

  try:
    user_number = int(user_input)
  except:
    i -= 1
    print("Invalid input")
    continue
  
  print((user_number % 2 == 0) and "even" or "odd")

  numbers.append(user_number)

  if user_number == 50:
    break

  if user_number > 10:
    moreThan10 += 1

print()
print("avg: " + str(sum(numbers) / len(numbers)))
print("more than 10: " + str(moreThan10))
