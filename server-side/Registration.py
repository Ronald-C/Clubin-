# Registration helper

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

	def addStudent(self, studentID, studentEmail, FirstName, LastName, MiddleName=None):
		try:
			# Validate method arguments
			Validate({
				'SJSUID': studentID,
				'FirstName': FirstName,
				'LastName': LastName,
				'MiddleName': MiddleName
			})

			self.session.execute("""
				SELECT * FROM Student WHERE Student.`SJSUID` = %s;
				""", studentID)

			exist = self.session.fetchone()
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
			self.conn.rollback()
			
			# A non-existing organization was specified!!!
			self._printError("%s", e)

	@staticmethod
	def _printWarning(message, *args):
		global DEBUG
		if 'DEBUG' in globals() and DEBUG:
			message = "[WARNING] " + str(message)
			print message % args

	@staticmethod
	def _printError(message, *args):
		global DEBUG
		# Print traceback if debugging ON
		if 'DEBUG' in globals() and DEBUG:
			print traceback.format_exc()
