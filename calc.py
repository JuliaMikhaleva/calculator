#simple div

input_str = input("One line with one operation: ")

operations = []
variables = []
was_digit = False
str_a = ""

for letter in input_str:
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

priorities = {
	3:("^",),
	2:("*", "/"),
	1:("+", "-")
}

error, error_val = False, None
for priority in range(3, 0, -1):
	if error:
		break
	new_variables = [variables[0]]
	new_operations = []

	for i in range(len(operations)):
		op = operations[i]
		var = variables[i+1]
		if op not in priorities[priority]:
			new_variables.append(var)
			new_operations.append(op)
		else:
			result = new_variables[-1]
			if op == '/' and var == 0:
				error, error_val = True, "Zero division (INF)"
				break
			elif op == "^":
				result = result ** var
			elif op in "+-*/":
				result = eval(f"{result}{op}{var}")
			else:
				error, error_val = True, "Unsupported operation"
				break
			new_variables[-1] = result

	variables = new_variables
	operations = new_operations

if error:
	print(f"Error during execution, {error_val=}")
else:
	print(f"Result: {variables[0]}")
