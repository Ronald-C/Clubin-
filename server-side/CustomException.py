# Custom Exception class for Validator module

class ValidatorException(Exception):
	""" A custom Exception class for validation

	Validation against a schema may return multiple validation errors
	that have to be sorted, where only high priority ones are kept.
	"""

	def __init__(self, *args):
		super(ValidatorException, self).__init__()

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
		# 	Parse args list and return list of high priority arguments only, ignoring all else
		# 

		self.args = errList
