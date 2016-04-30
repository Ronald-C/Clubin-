# Registration helper

import traceback
from stormpath.client import Client
from os import environ, path

from Connector import Database
from Validater import Validate
from CustomException import ValidatorException

DEBUG = True

abspath = path.dirname(path.abspath(__file__))

# Create a new Stormpath Client.
apiKeys = path.join(abspath, '../security/apiKey.properties')
client = Client(api_key_file_location=apiKeys)
href = environ['STORMPATH_APPLICATION_HREF']

# Retrieve our application
stormApp = client.applications.get(href)


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

	def _addStudent(self, studentID, studentEmail, FirstName, LastName, Password, MiddleName=None):
		errors = { 'SUCCESS': '', 'ERROR': '' }     # status return

		try:
			# Check stormpath for existance of account
			self.__verifyStormpathAccount(studentEmail)

			# Validate method arguments
			Validate({
				'SJSUID': studentID,
				'FirstName': FirstName,
				'LastName': LastName,
				'MiddleName': MiddleName,
				'Email': studentEmail
			})

			exist = self.__existingUser(studentEmail)		# Check if existing user

			if not exist:
				# Insert student entity
				self.session.execute("""
				INSERT INTO `Student` (`SJSUID`, `Email`, `FirstName`, `LastName`,
						`MiddleName`) VALUES (%s, %s, %s, %s, %s);
						""", (studentID, studentEmail, FirstName, LastName, MiddleName) ) 

				self.conn.commit()

				try:
					 # Create a new Stormpath Account.
					account = stormApp.accounts.create({
					    'given_name': FirstName,
					    'middle_name': MiddleName,
					    'surname': LastName,
					    'email': studentEmail,
					    'password': Password
					})

				except Exception as e:
					# Stormpath.accounts.create raises error on failure
					errors['SUCCESS'] = '0'
					errors['ERROR'] = str(e)

					raise TypeError(errors)


				errors['SUCCESS'] = '1'
				return errors

			else:	# Student entity already exists
				errors['SUCCESS'] = '0'
				errors['ERROR'] = 'Please verify inputs'

				raise TypeError(errors)

		except (TypeError, ValidatorException) as e:
			self.conn.rollback()
			# Unknown studentID or organizationName was encountered

			self._printWarning("%s", e)

			if isinstance(e, ValidatorException):
				errors['SUCCESS'] = '0'
				errors['ERROR'] = str(e)

				return errors
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
			return False
		

	def __existingUser(self, email):
		self.session.execute("""
			SELECT * FROM Student WHERE Student.`Email` = %s;
			""", email)

		exist = self.session.fetchone()

		if exist:
			return True

		return False


	def __verifyStormpathAccount(self, studentEmail):
		# Query stormpath if user exists
		stormAccount = stormApp.accounts.search({
		    'email': studentEmail
		})        

		if len(stormAccount) == 1:       # Account exists
			errors['SUCCESS'] = '0'
			errors['ERROR'] = 'Please verify inputs'

			raise TypeError(errors)
		
		else:
			return None


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


class Authentication(Database):
	"""
	A class that authenticates accounts for login
	
	"""
	def __init__(self):
		super(Authentication, self).__init__()
		# Get connection & cursor from Database
		self.conn = super(Authentication, self).connect()
		self.session = super(Authentication, self).getSession()

	