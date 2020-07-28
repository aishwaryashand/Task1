import sys

class A:
	def __init__(self, module_name, dob, roll_no):
		module = __import__(module_name)
		path,content = module.login(dob,roll_no)
		print(path)
		print(content)

A(sys.argv[1],sys.argv[2],sys.argv[3])

