#!/bin/python

from Officer import Officer #inheriting Officer Class

# Admin class declaration
class Admin(Officer): 
	# initialzie object "self" this allows 
	# to call inherited functions from Student and Officer class			
	def _init_(self): 
			super(Admin, self)._init_() 


	def deActivateStudent(self,uidStudent):
 	# changes the active status of the student based on thier UID
 	# searches the student that needs to get deactivated
		self.session.execute("""UPDATE MemberOf
					SET MemberOf.`Active` = '0'
					WHERE MemberOf.`Student_fk` = %s  
						""" % (uidStudent))
		self.conn.commit()

		# function that inserts into the black list for an organization
	def isTroubleMaker(self,uidStudent, uidOfficer, uidOrganization): 
		self.session.execute("""INSERT INTO TroubleMaker(Student_fk,Officer_fk,Organization_fk)
					VALUES(%s,%s,%s)""" , (uidStudent,uidOfficer,uidOrganization))
		self.conn.commit()
	 # updating an organization info
	 # updates Name,Description,Building, RoomNumber based on the orgID number
	def orgInfo(self,orgID,orgName,Descrip,Building,RoomNumber):
		self.session.execute("""UPDATE Organization 
					SET Organization.`OrganizationName` = %s, Organization.`Description` = %s,
					Organization.`Building` = %s ,
					Organization.`RoomNumber` = %s  
					WHERE Organization.`OrganizationID` = %s
					""", (orgID,orgName,Descrip,Building,RoomNumber)) 
		self.conn.commit()


	# check if student with specific foreign key 
	# is an Officer of AdminRank
	def isAdmin(self,AdminR): 

		self.session.execute("""SELECT AdminRank
								From OfficerOf
								Where Student_fk = %s """ % AdminR)
		self.conn.commit()
		 # note : fetchone() grabs the next row of a query
		AdminR = self.session.fetchone()
		# if student is not of AdminRank {President, Vice PRes}
		if not AdminR:
			raise TypeError("Student is not an Admin") 

		else:
			AdminR = AdminR['AdminRank']
			return str(AdminR)

	def isMemberOf(self,)