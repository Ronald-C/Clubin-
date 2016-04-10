# Validator

from cerberus import Validator

from CustomException import *

class Validate(object):
	""" Validation class using cerberus
	
	Takes json structured inputs to validate, raising errors if any
	A non-return indicates everything is valid
	"""

	SJSUID = {
		'SJSUID': {
			'required': True,
			'type': 'string',
			'maxlength': 9,
			'minlength': 9
		}
	}

	OrganizationName = {
		'OrganizationName': {
			'required': True,
			'type': 'string',
			'minlength': 3,
			'maxlength': 45
		}
	}

	StudentComment = {
		'StudentComment': {
			'required': True,
			'type': 'string',
			'minlength': 2,
			'maxlength': 200
		}
	}

	ArticleID = {
		'ArticleID': {
			'required': True,
			'type': 'string'
		}
	}

	def __init__(self, document):
		super(Validate, self).__init__()
		
		self.v = Validator()	
		self.__validate(document)

	def __validate(self, document):
		if not isinstance(document, dict):
			raise TypeError("Validate document expect class dict")

		schema = {}

		# Build schema rules
		for key in document.keys():
			if key is 'SJSUID':
				schema['SJSUID'] = Validate.SJSUID['SJSUID']

			elif key is 'OrganizationName':
				schema['OrganizationName'] = Validate.OrganizationName['OrganizationName']

			elif key is 'ArticleID':
				schema['ArticleID'] = Validate.ArticleID['ArticleID']

			elif key is 'StudentComment':
				schema['StudentComment'] = Validate.StudentComment['StudentComment']
				
			# 
			# NOTE:
			# 	ADD HERE, if extending rules schema
			# 

		if not schema:	# Check if empty rules list
			raise TypeError("Validating against empty schema")

		validStatus = self.v.validate(document, schema)

		if not validStatus:		# Status contains False if failed to meet rules
			raise ValidatorException({'ValidatorException': self.v.errors})
