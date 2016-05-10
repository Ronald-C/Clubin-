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

	def _addStudent(self, studentID, studentEmail, FirstName, LastName, Major, Password, MiddleName=None): # major to attributes
		errors = { 'SUCCESS': '', 'ERROR': '' }     # status return

		try:
			# Validate method arguments
			Validate({
				'SJSUID': studentID,
				'FirstName': FirstName,
				'LastName': LastName,
				'Major': Major,				# validates major
				'MiddleName': MiddleName,
				'Email': studentEmail
			})
			
			# Check stormpath for existance of account
			stormAccount = stormApp.accounts.search({
			    'email': studentEmail
				})        

			if len(stormAccount) >= 1:       # Account exists
				raise TypeError('Please verify inputs')


			exist = self.__existingUser(studentEmail)		# Check if existing user

			if not exist:
				# Insert student entity
				self.session.execute("""
					INSERT INTO `Student` (`SJSUID`, `Email`, `FirstName`, `MIddleName`,`LastName`,
						`Major`) VALUES (%s, %s, %s, %s, %s,%s);										
					""", (studentID, studentEmail, FirstName, MiddleName,LastName,Major)) #fixed insert query to incorporate major for the student


				try:
					 # Create a new Stormpath Account.
					account = stormApp.accounts.create({
					    'given_name': FirstName,
					    'middle_name': MiddleName,
					    'surname': LastName,
					    'email': studentEmail,
					    'password': Password
					})

					self.conn.commit()

					# Everything is OK
					errors['SUCCESS'] = '1'
					return errors

				except Exception as e:
					# Stormpath.accounts.create raises error on failure
					self.conn.rollback()
					raise TypeError(str(e))

			else:
				# Student entity already exists
				raise TypeError('Please verify inputs')

		except (TypeError, ValidatorException) as e:
			self.conn.rollback()

			self._printWarning("%s", e)

			errors['SUCCESS'] = '0'
			errors['ERROR'] = str(e)

			return dict(errors)

		except Exception as e:
			self.conn.rollback()
			
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

	def _authorize(self, username, password):
		errors = { 'SUCCESS': '', 'ERROR': '' }     # status return

		username = str(username).strip()
		password = str(password).strip()

		# Is username SJSUID or email ???
		isSJSUID = username.replace(' ', '').isdigit()

		try:
			# Check if the user is present
			if isSJSUID:

				Validate({'SJSUID': username})

				self.session.execute("""
					SELECT * FROM Student WHERE Student.`SJSUID` = %s;
					""", username)

				exist = self.session.fetchone()
				if exist and 'Email' in exist:
					username = exist['Email']

			else:	# username is an email
				Validate({'Email': username})

				self.session.execute("""
					SELECT * FROM Student WHERE Student.`Email` = %s;
					""", username)

				exist = self.session.fetchone()			# user is in database
			
			# Confirm stormpath account
			if exist:
				try:
					# Stormpath raises error on failure
					a = stormApp.authenticate_account(username, password).account
					if a.email:
						errors['SUCCESS'] = '1'

						return errors

				except Exception as e:
					raise TypeError('Invalid username or password')

		except (TypeError, ValidatorException) as e:
			self._printWarning("%s", e)

			errors['SUCCESS'] = '0'
			errors['ERROR'] = str(e)

			return dict(errors)

		except Exception as e:
			self._printError("%s", e)
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
