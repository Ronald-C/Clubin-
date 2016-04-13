# Officer entity (inherits Student)

from Student import Student
from Validater import *

class Officer(Student):
	""" A class that defines an Officer entity

	An officer is a special student that regulates a organization 
	They rank higher than members but not administrators
	"""
	def __init__(self):
		# Get connection & cursor from Database class
		super(Officer, self).__init__()

	def authorArticle(self, studentID, organizationName, articleTitle, articleContent):
		try:
			# Validate method arguments
			Validate({
				'SJSUID': studentID,
				'ArticleTitle': articleTitle,
				'ArticleContent': articleContent
			}) 

			# Get organization unique id
			uidOrganization = self._getOrganizationUID(organizationName)

			# Get student unique id
			uidStudent = self._getStudentUID(studentID)

			# Check active status of this officer
			active = self._isOfficerActive(uidStudent, uidOrganization)
			if not active:
				raise TypeError("Given studentID not allowed to author articles")

			else:	# Insert newsfeed article into DB 
				self.session.execute("""
					INSERT INTO NewsfeedArticle (`ArticleTitle`, `OrganizationID`, `ArticleContent`)
						VALUES (%s, %s, %s);
					""", (articleTitle, uidOrganization, articleContent))

				self.conn.commit()
				return True

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

	def _isOfficerActive(self, uidStudent, uidOrganization):
		# NOTE: An active entry in OfficerOf table means they are an officer
		self.session.execute("""
			SELECT * FROM OfficerOf as off
				WHERE off.`Student_fk` = %s AND off.`Organization_fk` = %s
				AND off.`Active` = '1'
			""", (uidStudent, uidOrganization))

		self.conn.commit()

		active = self.session.fetchone()
		if active:
			return True;

		return False

