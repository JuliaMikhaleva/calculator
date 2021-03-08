#simple div

input_str = input("One line with one operation: ")

result = 0
operation = "+"
was_digit = False
str_a = ""

for letter in input_str:
	if letter in "0123456789":
		was_digit = True
	if letter in "+-/*^" and was_digit:
		delitel = float(str_a)
		if operation == '/':
			if delitel == 0:
				result = "Inf"
			else:
				result = result / delitel
		elif operation == "+":
			result = result + delitel
		elif operation == "*":
			result = result * delitel
		elif operation == "-":
			result = result - delitel
		elif operation == "^":
			result = result ** delitel
		else:
			result = None
		operation = letter
		was_digit = False
		str_a = ""
	else:
		str_a += letter

delitel = float(str_a)
if operation == '/':
	if delitel == 0:
		result = "Inf"
	else:
		result = result / delitel
elif operation == "+":
	result = result + delitel
elif operation == "*":
	result = result * delitel	
elif operation == "-":
	result = result - delitel	
elif operation == "^":
	result = result ** delitel
else:
	result = None
		
print("Result: " + str(result))