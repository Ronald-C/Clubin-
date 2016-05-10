# Validator

import re
import sys
from cerberus import Validator

from CustomException import ValidatorException

class Validate(object):
	""" Validation class using cerberus 
	
	Takes json structured inputs to validate, raising errors if any
	A non-return indicates everything is valid
	"""

	SCHEMA_RULES = {
		'SJSUID': {
			'required': True,
			'type': 'string',
			'maxlength': 9,
			'minlength': 9
		},
		'OrganizationName': {
			'required': True,
			'type': 'string',
			'minlength': 3,
			'maxlength': 45
		},
		'StudentComment': {
			'required': True,
			'type': 'string',
			'minlength': 2,
			'maxlength': 200
		},
		'ArticleTitle': {
			'required': True,
			'type': 'string',
			'minlength': 8,
			'maxlength': 100
		},
		'ArticleContent': {
			'required': True,
			'type': 'string',
			'minlength': 8,
			'maxlength': 4000
		},
		'FirstName': {
			'required': True,
			'type': 'string',
			'minlength': 2,
			'maxlength': 45
		},
		'LastName': {
			'required': True,
			'type': 'string',
			'minlength': 2,
			'maxlength': 45
		},
		'MiddleName': {		# Optional 
			'nullable': True,
			'type': 'string',
			'maxlength': 25
		},
		'Department': {
			'required': True,
			'type': 'string',
			'minlength': 3,
			'maxlength': 45
		},
		'Major': {	# Validation for the students Major it is optional
			'required': True,
			'type': 'string',
			'minlength': 3,
			'maxlength': 45
		}
	}

	def __init__(self, document):
		super(Validate, self).__init__()
		
		self.v = Validator()	
		self.__validate(document)

	def __validate(self, document):
		if not isinstance(document, dict):
			raise TypeError("Validate document expect class dict")

		schema = {}		# The rules that dictate format of document
		errors = {}		# Any errors as a result of validation

		# Verify email formatting
		gotEmail = 'Email' in document

		if gotEmail:
			EMAIL_REGEX = re.compile(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$")
			
			if not EMAIL_REGEX.match(document['Email']):
				errors['EmailValidation'] = "Email does not meet requirements"

			del document['Email']	# Remove Email in document before validation

		# Build schema rules if exists
		for key, value in document.iteritems():	
			if key in Validate.SCHEMA_RULES:
				schema[key] = Validate.SCHEMA_RULES[key]

			else:
				raise TypeError("Validation rule not found!!!!")
				sys.exit(3)

		# Check if empty rules list before validating
		if not schema and not gotEmail:
			raise TypeError("Validating against empty schema")
		else:
			validStatus = self.v.validate(document, schema)

		# Status contains False if failed to meet rules
		if not validStatus:
			errors['ValidatorException'] = self.v.errors


		# Verify SJSUID is numeric
		if 'SJSUID' in document:
			numericSJSUID = str(document['SJSUID']).isdigit()
			
			if not numericSJSUID:
				if 'ValidatorException' in errors:

					errors['ValidatorException']['SJSUID'] = [
						errors['ValidatorException']['SJSUID'], 'Not numeric']

				else:
					errors['ValidatorException'] = {'SJSUID': 'Not numeric'}

		if errors:
			raise ValidatorException(errors)
