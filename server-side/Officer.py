# Officer entity (inherits Student)

from Student import Student
from Validater import Validate

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
			uidOrganization = super(Officer, self)._getOrganizationUID(organizationName)

			# Get student unique id
			uidStudent = super(Officer, self)._getStudentUID(studentID)

			# Check active status of this officer
			active = self._isOfficerActive(uidStudent, uidOrganization)
			if not active:
				raise TypeError("Given studentID not allowed to author articles")

			else:	# Insert newsfeed article into DB 
				self.session.execute("""
					INSERT INTO NewsfeedArticle (`ArticleTitle`, `OrganizationID`, `ArticleContent`)
						VALUES (%s, %s, %s);
					""", (articleTitle.strip(), uidOrganization, articleContent.strip()))

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


	def leaveOffice(self, studentID, organizationName):
		# Leaving officer position does not mean quitting organization
		try:
			# Validate method arguments
			Validate({
				'SJSUID': studentID,
				'OrganizationName': organizationName
			})

			# Get student unique id
			uidStudent = super(Officer, self)._getStudentUID(studentID)

			# Get organization unique id
			uidOrganization = super(Officer, self)._getOrganizationUID(organizationName)

			self.conn.commit()	# Being new transaction

			# Change officer status to inactive(0)
			self.session.execute("""
				UPDATE OfficerOf
					SET `Active` = '0'
					WHERE OfficerOf.`Student_fk` = %s AND OfficerOf.`Organization_fk` = %s;
				""", (uidStudent, uidOrganization))
			
			self.conn.commit()
			return True

<<<<<<< HEAD
		#except (TypeError, ValidaterException) as e:
		#	self.conn.rollback()
			# Unknown studentID or organizationName was encountered
		#	self._printWarning("%s", e)
=======
		except (TypeError, ValidatorException) as e:
			self.conn.rollback()
			# Unknown studentID or organizationName was encountered
			self._printWarning("%s", e)
>>>>>>> master
 
			#
			# TODO:
			#	return message to frontend of error
			#	return to frontend high priority validation errors
			# 
<<<<<<< HEAD
		#	return e
=======
			return e
>>>>>>> master

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
<<<<<<< HEAD
=======


o = Officer()
print o.leaveOffice('007810023', 'sce')
>>>>>>> master
