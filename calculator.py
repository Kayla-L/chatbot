import re

calculations = [
  "2 + 2",
  "1.1 + 6",
  "4 + 5",
  "4+6",
  "1 + 4 + 8 + 10.4"
]

"""
Assume that there are some numbers being added together and do the calculation.
1. first try to get this to work on just 2 numbers
2. once that is working, try for more than 2 numbers

Hints:
useful functions:
- float is a function that changes a string to a number so you can calculate in
  python
- split is a method of a string that breaks up a string into a list of strings
"""

def add(calc):
  # decide what numbers are being added together
  # numbers_being_added = []
  # for word in calc.split():
  #   if word.isdecimal():
  #     numbers_being_added.append(int(word))
  # print(numbers_being_added)
  numbers_being_added = re.findall('\d*\.?\d+', calc)
  # print(numbers_being_added)
  # convert those numbers to the correct type (e.g. "float")
  floats_being_added = []
  for item in numbers_being_added:
    floats_being_added.append(float(item))
  # print(floats_being_added)
  # add the numbers together
  answer_sum = sum(floats_being_added)
  # return the answer
  return answer_sum

# example_calc = "1 + 4 + 8 + 10.4"
# example_answer = calculate(example_calc)
# print(example_answer)