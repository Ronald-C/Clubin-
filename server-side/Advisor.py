#Advisor

import traceback

from Connector import Database
from Validater import Validate
from CustomException import ValidatorException

DEBUG = False

class Advisor(Database):

	def __init__(self):
		super(Advisor, self).__init__()

		self.conn = super(Advisor, self).connect()
		self.session = super(Advisor, self).getSession()

	def addAdvisor(self, FirstName, LastName, Email, Department, MiddleName=None):
		try:
			# Validate arguments
			Validate({
				'FirstName': FirstName,
				'LastName': LastName,
				'Department': Department,
				'MiddleName': MiddleName,
				'Email': Email
			})
			
			# Check if this advisor (professor) already exists in DB
			self.session.execute("""
				SELECT * FROM Advisor as ad
					WHERE ad.`FirstName` = %s AND ad.`LastName` = %s
					AND ad.`Email` = %s AND ad.`Department` = %s;
				""", (FirstName, LastName, Email, Department))

			exist = self.session.fetchone()
			if not exist:
				# Insert advisor if not exists
				self.session.execute("""
					INSERT INTO `Advisor` (`FirstName`, `MiddleName`,
						`LastName`, `Email`, `Department`) VALUES (%s, %s, %s, %s, %s);
					""", (FirstName, MiddleName, LastName, Email, Department))

				self.conn.commit()
				return True
				
			else:	# Advisor entity already exists
				raise TypeError("Advisor already registered")

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
	
	def editAdvisor():
		pass


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
