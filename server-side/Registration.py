# Registration helper

import traceback

from Connector import Database
from Validater import Validate
from CustomException import ValidatorException

DEBUG = True

class Registration(Database):
	""" A class that registers new student accounts

	To create a student account for a user, include this module
	and use methods to insert account information about user.
	"""
	def __init__(self):
		super(Registration, self).__init__()
		# Get connection & cursor from Database
		self.conn = super(Registration, self).connect()
		self.session = super(Registration, self).getSession()

	def _addStudent(self, studentID, studentEmail, FirstName, LastName, MiddleName=None):
		try:
			# Validate method arguments
			self._validate(studentID, studentEmail, FirstName, LastName, MiddleName)

			exist = self.existingUser(studentEmail)		# Check if existing user

			if not exist:
				# Insert student entity
				self.session.execute("""
				INSERT INTO `Student` (`SJSUID`, `Email`, `FirstName`, `LastName`,
						`MiddleName`) VALUES (%s, %s, %s, %s, %s);
						""", (studentID, studentEmail, FirstName, LastName, MiddleName) ) 

				self.conn.commit()
				return True

			else:	# Student entity already exists
				raise TypeError("Student already registered")

		except (TypeError, ValidatorException) as e:
			self.conn.rollback()
			# Unknown studentID or organizationName was encountered

			self._printWarning("%s", e)

			#
			# TODO:
			#	return message to frontend of error
			#	return to frontend high priority validation errors
			# 
			return e

		except Exception as e:
			print 'asd'
			self.conn.rollback()
			
			# A non-existing organization was specified!!!
			self._printError("%s", e)
			return False


	def _validate(self, studentID, studentEmail, FirstName, LastName, MiddleName=None):
		try:	
			Validate({
				'SJSUID': studentID,
				'FirstName': FirstName,
				'LastName': LastName,
				'MiddleName': MiddleName,
				'Email': studentEmail
			})
		
		except ValidatorException as e:
			self._printWarning("%s", e)


	def existingUser(self, email):
		self.session.execute("""
			SELECT * FROM Student WHERE Student.`Email` = %s;
			""", email)

		exist = self.session.fetchone()

		if exist:
			return True

		return False


	@staticmethod
	def _printWarning(message, *args):
		if DEBUG:
			message = "[WARNING] " + str(message)
			print message % args

	@staticmethod
	def _printError(message, *args):
		# Print traceback if debugging ON
		if DEBUG:
			print traceback.format_exc()
