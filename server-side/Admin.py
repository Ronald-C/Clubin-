from Officer import Officer
from Student import Student
#from Validater import Validate

class Admin(Officer):

	def _init_(self):
			

			super(Admin, self)._init_()

	def addStudent(self, SJSUID, Email, FirstName, MiddleName, LastName):

		#uidStudent = super(Admin, self)._getStudentUID(SJSUID)

		
		self.session.execute(""" 
			INSERT INTO Student (SJSUID, Email, FirstName,MiddleName, LastName) 
				VALUES (%s,%s,%s,%s,%s)""", (SJSUID,Email,FirstName, MiddleName,LastName))
		self.conn.commit()
		



