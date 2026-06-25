# -*- coding: utf-8 -*-
import random

user_range_upper = int(input("enter a upper range :"))
user_range_lower = int(input("enter a lower range :"))
generate_random_number = random.randint(user_range_lower,user_range_upper )
print(generate_random_number)

guess = 0
attempts = 0
while attempts <=6:
  attempts +=1
  print(f"This is your {attempts} attempt:")
  guess = int(input("enter your guess :"))
  range = guess - generate_random_number
  if guess == generate_random_number:
    print("you won ")
    break

  if guess > generate_random_number :
    if range <= 20:
        print("number is high")
    elif range >= 50:
      print("too high")


  elif  guess <  generate_random_number:
      if range <= -50:
        print("too low")
      else:
        print("low")

  if guess == generate_random_number:
    print("you won ")
    break