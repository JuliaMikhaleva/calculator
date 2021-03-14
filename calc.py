#simple div

input_str = input("One line with one operation: ")

operations = []
variables = []
was_digit = False
str_a = ""

for i in range(len(input_str)):
	letter = input_str[i]
	if letter in "0123456789":
		was_digit = True
	if letter in "+-/*^" and was_digit:
		operations.append(letter)
		variables.append(float(str_a))
		was_digit = False
		str_a = ""
	else:
		str_a += letter

variables.append(float(str_a))
result = variables[0]
for i in range(len(operations)):
	if result is None or type(result) is str:
		break
	op = operations[i]
	var = variables[i+1]
	if op == '/' and var == 0:
		result = "Inf"
	elif op == "^":
		result = result ** var
	elif op in "+-*/":
		result = eval(f"{result}{op}{var}")
	else:
		result = None
		
print("Result: " + str(result))