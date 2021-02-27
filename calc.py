#simple div
str_input = input("Delimoe: ")
delimoe = int(str_input)

operation = input ("+ / * - ^: ")
str_input2 = input("Delitel: ")
delitel = int(str_input2)

result = None
if operation == '/':
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