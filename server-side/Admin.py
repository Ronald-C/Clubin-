from Officer import Officer #inheriting Officer Class
#from Student import Student #inherting Student Class
#from Validater import Validate

class Admin(Officer): # Admin class declaration

	def _init_(self): # initialzie object "self" this allows to call inherited functions from Student and Officer class			

			super(Admin, self)._init_() #

	def addStudent(self, SJSUID, Email, FirstName, MiddleName, LastName):
		
		self.session.execute(""" 
			INSERT INTO Student (SJSUID, Email, FirstName,MiddleName, LastName) 
				VALUES (%s,%s,%s,%s,%s)""", (SJSUID,Email,FirstName, MiddleName,LastName))
		self.conn.commit()
		
	def deleteStudent(self, SJSUID):

		self.session.execute("""
			DELETE from Student where SJSUID='%s'; """ % SJSUID)
		self.conn.commit()

	#def promoteStudent(self, SJSUID):

	#	self.session.execute(""")
