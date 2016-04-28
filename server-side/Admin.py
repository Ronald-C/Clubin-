from Officer import Officer #inheriting Officer Class


class Admin(Officer): # Admin class declaration

	def _init_(self): # initialzie object "self" this allows to call inherited functions from Student and Officer class			

			super(Admin, self)._init_() #super allows us to call functions from the Parent's Parent's class 

	def addStudent(self, SJSUID, Email, FirstName, MiddleName, LastName): # addStudent function for Admin class
		"""This function allows an Admin to sign a student up to an Organization"""

		self.session.execute(""" 
			INSERT INTO Student (SJSUID, Email, FirstName,MiddleName, LastName) 
				VALUES (%s,%s,%s,%s,%s)""", (SJSUID,Email,FirstName, MiddleName,LastName)) 	# MySQL instance to add a student into the database
		self.conn.commit()
		
	def deleteStudent(self, SJSUID):	# function to delete a student from the database

		self.session.execute("""
			DELETE from Student where SJSUID='%s'; """ % SJSUID)	# MySQL Instance of deleting a student using their Student ID to be removed from the database
		self.conn.commit()
