# Student entity

import traceback
import re

from Connector import Database
from Validater import Validate
from CustomException import ValidatorException

DEBUG = False

class Student(Database):
	"""	A class the defines the Student entity  
		
	Student provides all methods a regular user can initiate.
	This class is to be inherited by higher ranking students.
	"""

	def __init__(self):
		super(Student, self).__init__()
		# Get connection & cursor from Database
		self.conn = super(Student, self).connect()
		self.session = super(Student, self).getSession()

	def getStudentInfo(self, username):
		username = str(username)

		# Is username SJSUID or email ???
		isSJSUID = username.replace(' ', '').isdigit()

		studentInfo = {}
		try:
			# Check if the user is present
			if isSJSUID:
				self.session.execute("""
					SELECT * FROM Student WHERE Student.`SJSUID` = %s;
					""", username)

			else:	# username is an email
				self.session.execute("""
					SELECT * FROM Student WHERE Student.`Email` = %s;
					""", username)
			
			details = self.session.fetchone()
			if details:		# Get Student table
				studentInfo['Student'] = details
				uid = details['UID']
			
			else:	# If nothing returned == student not found
				return False

			# Get organization student is member of
			self.session.execute("""
				SELECT org.OrganizationID, org.OrganizationName FROM MemberOf as memOf 
					JOIN Organization as org WHERE memOf.`Organization_fk` = org.`OrganizationID`
					AND memOf.`Active` = '1' AND memOf.`Student_fk` = %s;
				""", uid)

			studentInfo['Organizations'] = self.session.fetchall()

			#All the student's interests
			studentInfo['Interests'] = self.getInterests(uid)

			#All the student's comments (count, not the words)
			studentInfo['CommentCount'] = self.getCommentCount(uid)

			#All the student's banned orgs (count, not the names)
			studentInfo['BanCount'] = self.getBanCount(uid)

			if studentInfo:		# Non-empty dict
				return studentInfo	

			else:
				return False

		except Exception as e:
			return False

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

	def editStudentInfo(self, studentID, **kwargs):
		try:
			# Validate arguments
			Validate({
				'SJSUID': studentID	
			})

			# Loop kwargs and do queries
			for key, value in kwargs.iteritems():
				if key == 'Email':
					self.__updateStudentEmail(studentID, value)

				# 
				# INSERT HERE IF ADDITIONAL STUDENT ATTRIBUTE EDIT FUNC
				# 

				else:	# Unknown key was passed to method
					raise TypeError("Student attribute not found")

			self.conn.commit()	# Commit transaction only after all changes applied
			return True

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

	def __updateStudentEmail(self, studentID, newStudentEmail):
		EMAIL_REGEX = re.compile(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$")

		if not EMAIL_REGEX.match(newStudentEmail):	# Validate email format
			raise TypeError("Student email update error")

		self.session.execute("""
			UPDATE Student 
			SET Student.`Email` = %s
				WHERE Student.`SJSUID` = %s;
			""", (newStudentEmail, studentID))

	def getInterests(self, uid):
		self.session.execute("""
			SELECT Interest.`InterestID`, Interest.`Title` FROM StudentInterest
				JOIN Interest ON StudentInterest.`Interest_fk` = Interest.`InterestID`
				WHERE StudentInterest.`Student_fk` = %s
			""", uid)

		manyThings = self.session.fetchall()

		if manyThings:
			return manyThings
		else:
			return ''		
	
	def getCommentCount(self, uid):
		self.session.execute("""
		SELECT
			COUNT(Author_fk) AS count
		FROM
			Comment
		WHERE
			Author_fk = %s""", uid)

		return self.session.fetchone()


	def getBanCount(self, uid):
		self.session.execute("""
		SELECT
			COUNT(Student_fk) AS count
		FROM
			TroubleMaker
		WHERE
			Student_fk = %s""", uid)

		return self.session.fetchone()

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
