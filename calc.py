#simple div

input_str = input("One line with one operation: ")

operation = None
str_a = ""
str_b = ""
for letter in input_str:
	if letter in "+-/*^":
		operation = letter
	else:
		if operation is None:
			str_a += letter
		else:
			str_b += letter

delimoe = float(str_a)
delitel = float(str_b)

result = None
if operation == '/':
	if delitel == 0:
		result = "Inf"
	else:
		result = delimoe / delitel
elif operation == "+":
	result = delimoe + delitel
elif operation == "*":
	result = delimoe * delitel	
elif operation == "-":
	result = delimoe - delitel	
elif operation == "^":
	result = delimoe ** delitel
else:
	result = None		

print("Result: " + str(result))