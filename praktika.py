"""
хотим калькулятор выражений - 2 + 3.5 * 2 - 3 ^ 2
"""

#считать строчку от пользователя
instr = input ("Что вычислить? ")


#почистить строку
# "-2 + 3.5 * 2 - 3 ^ 2" -> "-2+3.5*2-3^2"
instr_parsed= instr.replace (" ", "")


#распарсить
"""
на вход строку
"-2+3.5*2-3^2"

на выход список словарей с операциями +- и значениями
(+ * - ^)
(-2 3.5 2 3 2)
"""
hp_ops = tuple("^")
mp_ops = tuple("*/")
lp_ops = tuple("+-")
supported_ops = hp_ops + mp_ops + lp_ops
digit_chars = tuple("0123456789.-")

actions = list()
d = dict()
d["opr"] = "First"
d['val'] = ''
actions.append(d)

for i, letter in enumerate(instr):
	if letter in supported_ops and (i > 0) and actions [-1]["val"] != "":
		actions.append({"opr": letter, "val": ''})
		pass #под операции
	elif letter in digit_chars:
		actions[-1]["val"] += letter
		pass #под числа

#вычислить операции первого приоритета (возведение в степень)
"""
на вход наш набор значений и операций
на выход обновленная ? структура данных с операциями +- и значениями

-2+3.5*2-3^2
-2+3.5*2-9
"""
i = 0
actions.reverse()
while i < len(actions):
	action = actions[i]
	operation = action.get("opr")
	if operation in hp_ops:
		if operation == "^":
			pre_res = float(actions[i+1].get('val')) ** float(actions[i].get('val'))
			actions[i+1]['val'] =str(pre_res)
			del actions[i]
	else:
		i += 1

actions.reverse()

#вычислить операции второго приоритета (умножение и деление)
"""
на вход наш набор значений и операций
на выход обновленная ? структура данных с операциями +- и значениями

-2+3.5*2-9
-2+7-9
"""
i = 0
result = ""
error = False
while i < len(actions) and not error:
	action = actions[i]
	operation = action.get("opr")
	if operation in mp_ops:
		if float(action.get("val")) == 0 and operation == "/":
			result ="INF"
			error = True
		else:
			pre_res = eval("{0}{1}{2}".format(
				float(actions[i-1].get("val")),
				operation,
				float(actions[i].get("val"))
			))
			actions[i-1]["val"] = str(pre_res)
			del actions[i]
	else:
		i += 1

#вычислить операции третьего приоритета (сложение и вычитание)
"""
на вход наш набор значений и операций
на выход обновленная ? структура данных с операциями +- и значениями

2+3^2
2+9
"""

for action in actions:
	if not error:
		var_A = result
		var_B = action.get('val')
		operation = action.get('opr')
		if operation in lp_ops:
			result = eval(str(var_A) + operation + str(var_B))
		else:
			result = var_B

print("Результат: {}".format(result))