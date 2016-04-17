# Student entity

import traceback

from Connector import Database
from Validater import *

DEBUG = True 	# Set this variable for console print

class Student(Database):
	"""	A class the defines the Student entity  
		
	Student provides all methods a regular user can initiate.
	This class is to be inherited by higher ranking students.
	"""

	def __init__(self):
		# super(Student, self).__init__()
		# Get connection & cursor from Database
		self.conn = super(Student, self).connect()
		self.session = super(Student, self).getSession()

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
				return False

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

	def joinOrganization(self, studentID, organizationName):
		try:
			# Validate method arguments
			Validate({
				'SJSUID': studentID,
				'OrganizationName': organizationName
			})

			# Get student unique ID
			uidStudent = self._getStudentUID(studentID)

			# Get organization unique ID
			uidOrganization = self._getOrganizationUID(organizationName)

			self.conn.commit()	# Being new transaction

			# Check if student already organization member
			self.session.execute("""
				SELECT * FROM MemberOf as mem
					WHERE mem.`Student_fk` = %s AND mem.`Organization_fk` = %s;
				""", (uidStudent, uidOrganization))

			data = self.session.fetchone()
			self.conn.commit()	# Being new transaction

			if not data:	# Add student to organization 
				self.session.execute("""
					INSERT INTO MemberOf (`Student_fk`, `Organization_fk`)
						VALUES (%s, %s);
					""", (uidStudent, uidOrganization))

				self.conn.commit()
				return True

			else:	# Check if student active(1) member of organization	
				activeMember = self._isStudentActiveMember(uidStudent, uidOrganization)

				if not activeMember : # Update organization member active status to active(1)

					# Inactive status may be a result of being blacklisted
					blacklisted = self._isStudentBlacklisted(uidStudent, uidOrganization)	
					if blacklisted:
						return False

					self.session.execute("""
						UPDATE MemberOf
							SET MemberOf.`Active` = '1' 
							WHERE MemberOf.`Student_fk` = %s AND MemberOf.`Organization_fk` = %s;
						""", (uidStudent, uidOrganization))
									
					self.conn.commit()
					return True

				else:	# Organization member already active	
					self._printWarning("%s in %s already active", studentID, organizationName)
					return True

			return False 	# 99.99% chance you will not hit this !!!

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

	def quitOrganization(self, studentID, organizationName):
		try:
			# Validate method arguments
			Validate({
				'SJSUID': studentID,
				'OrganizationName': organizationName
			})

			uidStudent = self._getStudentUID(studentID)

			# Get organization unique ID
			uidOrganization = self._getOrganizationUID(organizationName)

			self.conn.commit()	# Being new transaction

			# Check if student active(1) member of organization
			activeMember = self._isStudentActiveMember(uidStudent, uidOrganization)			
		
			if activeMember: # Set organization member to inactive
				self.session.execute("""
					UPDATE MemberOf
						SET MemberOf.`Active` = '0' 
						WHERE MemberOf.`Student_fk` = %s AND MemberOf.`Organization_fk` = %s;
					""", (uidStudent, uidOrganization))
								
				self.conn.commit()
				return True

			else:	# Empty SQL return means either non-member or inactive
				self._printWarning("%s either inactive or not part of %s", studentID, organizationName)
				return True

			return False 	# 99.99% chance you will not hit this !!!

		except (TypeError, ValidatorException) as e:
			self.conn.rollback()
			# Unknown interest name. No InterestID returned
			self._printWarning("%s", e)
 
			#
			# TODO:
			#	return message to frontend of unknown interestName not foun
			#	return to frontend high priority validation errors
			# 
			return e

		except Exception as e:
			self.conn.rollback()
			
			# A non-existing organization was specified!!!
			self._printError("%s", e)

	def addInterest(self, studentID, *interests):
		try:
			# Validate method arguments
			Validate({
				'SJSUID': studentID
			})

			uidStudent = self._getStudentUID(studentID)

			values = []
			# Build list of (studentID, InterestID)
			for interest in interests:
				#  Get interest unique id
				self.session.execute("""
					SELECT i.`InterestID`
						FROM Interest as i WHERE i.`Title` = %s;
					""", interest)

				interestID = self.session.fetchone()

				if not interestID:	# No interestID found == Unknown interestName
					raise TypeError("Unknown interest")
				else:
					interestID = interestID['InterestID']

				# If duplicate entry exists, do not insert again else SQL IntegrityError
				self.session.execute("""
					SELECT * FROM StudentInterest as si
						WHERE si.`Student_fk` = %s AND si.`Interest_fk` = %s;
					""", (uidStudent, interestID))

				duplicate = self.session.fetchall()
				if not duplicate:
					values.append((uidStudent, interestID))
				
				else:	# Go on to next loop iteration
					continue

			self.conn.commit()	# Start a new transaction

			# Return false if no values to insert into DB
			if values:
				# Add all student's interest at once
				self.session.executemany("""
					INSERT INTO StudentInterest (`Student_fk`, `Interest_fk`)
						VALUES (%s, %s)
					""", values)

				self.conn.commit()
				return True

			return False

		except (TypeError, ValidatorException) as e:
			self.conn.rollback()
			# Unknown interest name. No InterestID returned
			self._printWarning("%s", e)
 
			#
			# TODO:
			#	return message to frontend of unknown interestName not foun
			#	return to frontend high priority validation errors
			# 
			return e

		except (ValidatorException, Exception) as e:
			self.conn.rollback()
			self._printError("%s", e)

	def removeInterest(self, studentID, *interests):
		try:
			# Validate method arguments
			Validate({
				'SJSUID': studentID
			})

			uidStudent = self._getStudentUID(studentID)

			values = []
			# Build list of (studentID, InterestID)
			for interest in interests:
				#  Get interest unique id
				self.session.execute("""
					SELECT i.`InterestID`
						FROM Interest as i WHERE i.`Title` = %s;
					""", interest)

				interestID = self.session.fetchone()

				if not interestID:	# No interestID found == Unknown interestName
					raise TypeError("Unknown interest")
				else:
					interestID = interestID['InterestID']

				values.append((uidStudent, interestID))

				# Return false if no values to enter into DB
				if values:
					# Delete rows with (studentID, interestID)
					# NOTE: DELETE will have no action if not found
					self.session.executemany("""
						DELETE FROM StudentInterest 
							WHERE StudentInterest.`Student_fk` = %s
							AND StudentInterest.`Interest_fk` = %s;
						""", values)

					self.conn.commit()
					return True

				return False

		except (TypeError, ValidatorException) as e:
			self.conn.rollback()
			# Unknown interest name. No InterestID returned
			self._printWarning("%s", e)
 
			#
			# TODO:
			#	return message to frontend of unknown interestName not foun
			#	return to frontend high priority validation errors
			# 
			return e

		except (ValidatorException, Exception) as e:
			self.conn.rollback()
			self._printError("%s", e)

	def commentArticle(self, studentID, studentComment, articleID):
		try:
			# Validate method arguments
			Validate({
				'SJSUID': studentID,
				'StudentComment': studentComment,
			})

			uidStudent = self._getStudentUID(studentID)

			# Get organization unique id indirectly from article
			self.session.execute("""
				SELECT nfa.`OrganizationID`
					FROM NewsfeedArticle as nfa WHERE nfa.`ArticleID` = %s;
				""", articleID)

			orgID = self.session.fetchone()
			if not orgID:
				raise TypeError("Unknown articleID")
			else:
				orgID = orgID['OrganizationID']

			# Verify that student is active member
			active = self._isStudentActiveMember(uidStudent, orgID)

			if active:	# Only active members can comment
				self.session.execute("""
					INSERT INTO Comment (`Article_fk`, `Author_fk`, `Content`)
						VALUES (%s, %s, %s);
					""", (articleID, uidStudent, studentComment))

				self.conn.commit()
				return True

			return False

		except (TypeError, ValidatorException) as e:
			self.conn.rollback()
			# Unknown studentID or articleID returned
			self._printWarning("%s", e)
 
			#
			# TODO:
			#	return message to frontend of unknown studentID and articleID
			#	return to frontend high priority validation errors
			# 
			return e

		except (ValidatorException, Exception) as e:
			self.conn.rollback()
			self._printError("%s", e)

	def editStudent(self, studentID, **kwargs):
		# 
		# TODO:
		# 	this method should be able to edit attributes of the Student entity
		# 
		pass

	def _isStudentActiveMember(self, uidStudent, uidOrganization):
		self.session.execute("""
			SELECT * FROM MemberOf as mem
				WHERE mem.`Student_fk` = %s	AND mem.`Organization_fk` = %s
				AND mem.`Active` = '1';

			""", (uidStudent, uidOrganization))

		self.conn.commit()	# Being new transaction

		active = self.session.fetchone()
		if active:
			return True

		return False

	def _isStudentBlacklisted(self, uidStudent, uidOrganization):
		self.session.execute("""
			SELECT * FROM TroubleMaker as t
				WHERE t.`Student_fk` = %s AND t.`Organization_fk` = %s;
			""", (uidStudent, uidOrganization))

		self.conn.commit()	# Being new transaction

		blacklisted = self.session.fetchone()
		if blacklisted:
			return True

		return False

	def _getStudentUID(self, studentID):
		# Get student unique ID
		self.session.execute("""
			SELECT s.`UID` FROM Student as s WHERE s.`SJSUID` = %s
			""", studentID)

		uidStudent = self.session.fetchone()
		if not uidStudent:
			raise TypeError("Unknown studentID")

		else:
			uidStudent = uidStudent['UID']
			return str(uidStudent)

	def _getOrganizationUID(self, organizationName):
		# Get organization unique ID
		self.session.execute("""
			SELECT o.`OrganizationID` FROM Organization as o WHERE o.`OrganizationName` = %s
			""", organizationName)

		uidOrganization = self.session.fetchone()
		if not uidOrganization:
			raise TypeError("Unknown organizationName")
		
		else:
			uidOrganization = uidOrganization['OrganizationID']
			return str(uidOrganization)

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
