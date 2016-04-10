# Student entity

import sys

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

			uidStudent = self.session.fetchone()['UID']

			# Get organization unique ID
			self.session.execute("""
				SELECT o.`OrganizationID` FROM Organization as o WHERE o.`OrganizationName` = %s
				""", organizationName)

			uidOrganization = self.session.fetchone()['OrganizationID']

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

		except (ValidatorException, Exception) as e:
			self.conn.rollback()
			
			if isinstance(e, ValidatorException):
				self._printWarning("ValidatorException %s", e)
				
				# 
				# TODO:
				# 	return to frontend high priority validation errors
				#
				return e

			else:	# A non-existing organization was specified!!!
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

			uidStudent = self.session.fetchone()['UID']

			# Get organization unique ID
			self.session.execute("""
				SELECT o.`OrganizationID` FROM Organization as o WHERE o.`OrganizationName` = %s
				""", organizationName)

			uidOrganization = self.session.fetchone()['OrganizationID']

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

		except (ValidatorException, Exception) as e:
			self.conn.rollback()
			
			if isinstance(e, ValidatorException):
				self._printWarning("ValidatorException %s", e)
				
				# 
				# TODO:
				# 	return to frontend high priority validation errors
				#
				return e

			else:	# A non-existing organization was specified!!!
				self._printError("%s", e)

	def commentArticle(self, studentID, studentComment, articleID):
		try:
			# Validate method arguments
			Validate({
				'SJSUID': studentID,
				'OrganizationName': organizationName,
				'ArticleID': articleID
			})

			# Get student unique ID
			self.session.execute("""
				SELECT s.`UID` FROM Student as s WHERE s.`SJSUID` = %s
				""", studentID)

			uidStudent = self.session.fetchone()['UID']

			# Get organization unique id
			self.session.execute("""
				SELECT nfa.`OrganizationID`
					FROM NewsfeedArticle as nfa WHERE nfa.`ArticleID` = %s;
				""", articleID)

			# Verify that student is active member
			orgID = self.session.fetchone()['OrganizationID']
			active = self._isStudentActiveMember(uidStudent, orgID)

			if active:	# Only active members can comment
				self.session.execute("""
					INSERT INTO Comment (`Article_fk`, `Author_fk`, `Content`)
						VALUES (%s, %s, %s);
					""", (articleID, uidStudent, studentComment))

				self.conn.commit()
				return True

			return False

		except (ValidatorException, Exception) as e:
			self.conn.rollback()
			
			if isinstance(e, ValidatorException):
				self._printWarning("ValidatorException %s", e)
				
				# 
				# TODO:
				# 	return to frontend high priority validation errors
				#
				return e

			else:
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
		if 'DEBUG' in globals() and DEBUG:
			message = "[ERROR] " + str(message)
			print message % args
		
		sys.exit(1)
