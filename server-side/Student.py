# Student entity

from cerberus import Validator
import sys

from Connector import Database
from CustomException import *

DEBUG = True 	# Set this variable for console print

class Student(Database):
	"""	A class the defines the Student entity  
		
	Student provides all methods a regular user can initiate.
	This class is to be inherited by higher ranking students.
	"""

	def __init__(self):
		self.conn = super(Student, self).connect()
		self.session = super(Student, self).getSession()

	def joinOrganization(self, studentID, organizationName):
		try:
			# Validate method arguments
			self.__vStudent_Organization(studentID, organizationName)

			# Check if student already organization member
			self.session.execute("""
				SELECT * FROM MemberOf as mem
					WHERE mem.`Student_fk` =
						(SELECT s.`UID` FROM Student as s WHERE s.`SJSUID` = %s)
					AND mem.`Organization_fk` = 
						(SELECT o.`OrganizationID` FROM Organization as o WHERE o.`OrganizationName` = %s);
				""", (studentID, organizationName))

			data = self.session.fetchone()
			
			if not data:	# Add student to organization 
				self.session.execute("""
					INSERT INTO MemberOf (`Student_fk`, `Organization_fk`)
						VALUES (
							(SELECT s.`UID` FROM Student as s WHERE s.`SJSUID` = %s),
							(SELECT o.`OrganizationID` FROM Organization as o WHERE o.`OrganizationName` = %s)
						);
					""", (studentID, organizationName))

				self.conn.commit()
				return True

			else:	# Check if student active(1) member of organization	
				activeMember = self._isStudentActiveMember(studentID, organizationName)

				if not activeMember : # Update organization member active status to active(1)
					# 
					# TODO:
					# 	member inactive(0) may be result of blacklist. If present, return False
					# 

					self.session.execute("""
						UPDATE MemberOf
							SET MemberOf.`Active` = '1' 
							WHERE MemberOf.`Student_fk` = 
								(SELECT s.`UID` FROM Student as s WHERE s.`SJSUID` = %s)
							AND MemberOf.`Organization_fk` =
								(SELECT o.`OrganizationID` FROM Organization as o WHERE o.`OrganizationName` = %s);
						""", (studentID, organizationName))
									
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

			else:
				self._printError("%s", e)

	def quitOrganization(self, studentID, organizationName):
		# Validate method arguments
		self.__vStudent_Organization(studentID, organizationName)
		
		try:
			# Check if student active(1) member of organization
			activeMember = self._isStudentActiveMember(studentID, organizationName)			
		
			if activeMember: 
				self.session.execute("""
					UPDATE MemberOf
						SET MemberOf.`Active` = '0' 
						WHERE MemberOf.`Student_fk` = 
							(SELECT s.`UID` FROM Student as s WHERE s.`SJSUID` = %s)
						AND MemberOf.`Organization_fk` =
							(SELECT o.`OrganizationID` FROM Organization as o WHERE o.`OrganizationName` = %s);
					""", (studentID, organizationName))
								
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

	def commentArticle(self, studentID, studentComment, articleID):
		try:
			# NOTE: articleID unique unlike articleName
			self.session.execute("""
				SELECT o.`OrganizationName`
					FROM Organization as o WHERE o.`OrganizationID` =   
					(SELECT nfa.`OrganizationID` FROM NewsfeedArticle as nfa WHERE nfa.`ArticleID` = %s);
				""", articleID)

			# Verify that student is active member
			orgName = self.session.fetchone()['OrganizationName']
			active = self._isStudentActiveMember(studentID, orgName)

			if active:	# Only active members can comment
				self.session.execute("""
					INSERT INTO Comment (`Article_fk`, `Author_fk`, `Content`)
						VALUES (%s, 
							(SELECT s.`UID` FROM Student as s WHERE s.`SJSUID` = %s), %s);
					""", (articleID, studentID, studentComment))

				self.conn.commit()
				return True

			return False

		except Exception as e:
			self.conn.rollback()
			self._printError("%s", e)

	def _isStudentActiveMember(self, studentID, organizationName):
		self.session.execute("""
			SELECT * FROM MemberOf as mem
				WHERE mem.`Student_fk` =
					(SELECT s.`UID` FROM Student as s WHERE s.`SJSUID` = %s)
				AND mem.`Organization_fk` = 
					(SELECT o.`OrganizationID` FROM Organization as o WHERE o.`OrganizationName` = %s)
				AND mem.`Active` = '1';
			""", (studentID, organizationName))

		active = self.session.fetchone()
		if active:
			return True

		return False

	@staticmethod
	def __vStudent_Organization(studentID, organizationName):
		schema = {
			'SJSU': {
				'required': True,
				'type': 'string',
				'maxlength': 9
			},
			'OrganizationName': {
				'required': True,
				'type': 'string',
				'minlength': 3,
				'maxlength': 45
			}
		}

		v = Validator()	
		validStatus = v.validate({
				'SJSU': studentID,
				'OrganizationName': organizationName
			}, schema)

		if not validStatus:		# Status contains False if failed to meet rules
			raise ValidatorException(v.errors)

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
