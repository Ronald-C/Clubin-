# Custom Exception class for Validator module

class ValidatorException(Exception):

	def __init__(self, *args):
		errList = []
		# Build error arguments into list
		for arg in args:
			if isinstance(arg, str):
				errList.append(arg)

			else:
				# Note: str() vs repr() 
				errList.append(str(arg))

		# 
		# TODO:
		# 	Multiple errors may be returned for one rule 
		# 	Parse args list and return priority arguments only, ignoring all else
		# 

		self.args = errList
