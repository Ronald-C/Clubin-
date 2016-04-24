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

		def __init__(self):
		# super(Student, self).__init__()
		# Get connection & cursor from Database
		self.conn = super(Student, self).connect()
		self.session = super(Student, self).getSession()
	#function for an Admin to add a student into the database
	def addStudent(self,studentID,studentEmail,FirstName,LastName,MiddleName=None):
		self.session.execute("""INSERT INTO Student (SJSUID, Email, FirstName,'MiddleName', 'LastName'))
		VALUES(SJSUID, Email, FirstName,MiddleName,LastName""")
	#function for an Admin to remove a student from an organization
	def quitOrganization(self, studentID, organizationName):
		self.session.execute("""DELETE from Student (SJSUID,Email,FirstName,'MiddleName', 'LastName'))
		VALUES(SJSUID, Email, FirstName,MiddleNme,LastName""")
	#function for an Admin to check if a student is an active member of the organization
	def _isStudentActiveMember(self, uidStudent, uidOrganization):
		self.session.execute("""
			SELECT * FROM MemberOf as mem
				WHERE mem, 'Student_fk' = %s AND mem.'Organization_fk' = %s
				AND mem.'Active' = '1'; 
				""", (uidStudent, uidOrganization))					 )

	