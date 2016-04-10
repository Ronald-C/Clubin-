# Student entity

import sys
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
		super(Student, self).__init__()
		self.conn = super(Student, self).connect()
		self.session = super(Student, self).getSession()

	def joinOrganization(self, studentID, organizationName):
		try:
			# Validate method arguments
			Validate({
				'SJSUID': studentID,
				'OrganizationName': organizationName
			})

			# Get student unique ID
			self.session.execute("""
				SELECT s.`UID` FROM Student as s WHERE s.`SJSUID` = %s
				""", studentID)

			uidStudent = self.session.fetchone()
			if not uidStudent:
				raise TypeError("Unknown studentID")
			else:
				uidStudent = uidStudent['UID']

			# Get organization unique ID
			self.session.execute("""
				SELECT o.`OrganizationID` FROM Organization as o WHERE o.`OrganizationName` = %s
				""", organizationName)

			uidOrganization = self.session.fetchone()
			if not uidOrganization:
				raise TypeError("Unknown organizationName")
			else:
				uidOrganization = uidOrganization['OrganizationID']

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

	def quitOrganization(self, studentID, organizationName):
		try:
			# Validate method arguments
			Validate({
				'SJSUID': studentID,
				'OrganizationName': organizationName
			})

			# Get student unique ID
			self.session.execute("""
				SELECT s.`UID` FROM Student as s WHERE s.`SJSUID` = %s
				""", studentID)

			uidStudent = self.session.fetchone()
			if not uidStudent:
				raise TypeError("Unknown studentID")
			else:
				uidStudent = uidStudent['UID']

			# Get organization unique ID
			self.session.execute("""
				SELECT o.`OrganizationID` FROM Organization as o WHERE o.`OrganizationName` = %s
				""", organizationName)

			# Will raise TypeError if unknown organizationName
			uidOrganization = self.session.fetchone()
			if not uidOrganization:
				raise TypeError("Unknown organizationName")
			else:
				uidOrganization = uidOrganization['OrganizationID']

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

			# Get student unique ID
			self.session.execute("""
				SELECT s.`UID` FROM Student as s WHERE s.`SJSUID` = %s
				""", studentID)

			uidStudent = self.session.fetchone()
			if not uidStudent:
				raise TypeError("Unknown studentID")
			else:
				uidStudent = uidStudent['UID']

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

			# Add all student's interest at once
			self.session.executemany("""
				INSERT INTO StudentInterest (`Student_fk`, `Interest_fk`)
					VALUES (%s, %s)
				""", values)

			self.conn.commit()
			return True

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

	def removeInterest(self):
		pass

	def commentArticle(self, studentID, studentComment, articleID):
		try:
			# Validate method arguments
			Validate({
				'SJSUID': studentID,
				'StudentComment': studentComment,
				'ArticleID': articleID
			})

			# Get student unique ID
			self.session.execute("""
				SELECT s.`UID` FROM Student as s WHERE s.`SJSUID` = %s
				""", studentID)

			uidStudent = self.session.fetchone()
			if not uidStudent:
				raise TypeError("Unknown studentID")
			else:
				uidStudent = uidStudent['UID']

			# Get organization unique id
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

