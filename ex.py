class Question : 
	answer = None
	text = None 

class Add(Question):
	def __init__(self, num1, num2):
		self.text = '{} + {}'.format(num1, num2)
		self.answer = num1 + num2 

from ex import Add
add1 = Add(1,2)
print(add1.text)
# print(add1.answer)