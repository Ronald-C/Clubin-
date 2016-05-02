from Officer import Officer #inheriting Officer Class


class Admin(Officer): # Admin class declaration

	def _init_(self): # initialzie object "self" this allows to call inherited functions from Student and Officer class			

			super(Admin, self)._init_() #super allows us to call functions from the Parent's Parent's class 


	def deActivateStudent(self,uidStudent):

		self.session.execute("""UPDATE MemberOf
					SET MemberOf.`Active` = '0' # changes the active status of the student based on thier UID
					WHERE MemberOf.`Student_fk` = %s  # searches the student that needs to get deactivated
						""" % (uidStudent))
		self.conn.commit()

	def isTroubleMaker(self,uidStudent, uidOfficer, uidOrganization): # function that inserts into the black list for an organization
		self.session.execute("""INSERT INTO TroubleMaker(Student_fk,Officer_fk,Organization_fk)
					VALUES(%s,%s,%s)""" , (uidStudent,uidOfficer,uidOrganization))
		self.conn.commit()
	
	def orgInfo(self,orgID,orgName,Descrip,Building,RoomNumber): # updating an organization info
		self.session.execute("""UPDATE Organization 
					SET Organization.`OrganizationName` = %s, Organization.`Description` = %s,
					Organization.`Building` = %s ,
					Organization.`RoomNumber` = %s  
					WHERE Organization.`OrganizationID` = %s
					""", (orgID,orgName,Descrip,Building,RoomNumber)) # updates Name,Description,Building, RoomNumber based on the orgID number
		self.conn.commit()
