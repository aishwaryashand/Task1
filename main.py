import sys
class A:
	def __init__(self,module_name):
		module = __import__(module_name)

A(sys.argv[1])
