# Admin Entity


# blacklist
# quit org.
# resign
# 
#
#
#
#
from Student import Student
from Validater import *

class Admin(Student):

	def _init_(self):

		super(Admin, self)._init_()
	#function for an Admin to add a student into the database
	def addStudent(self,studentID,studentEmail,FirstName,LastName,MiddleName=None):
		self.session.execute("""INSERT INTO Student (SJSUID, Email, FirstName,'MiddleName', 'LastName'))
		VALUES(SJSUID, Email, FirstName,MiddleName,LastName""")

	def quitOrganization(self, studentID, organizationName):
		self.session.execute("""DELETE from Student (SJSUID,Email,FirstName,'MiddleName', 'LastName'))
		VALUES(SJSUID, Email, FirstName,MiddleNme,LastName""")

	