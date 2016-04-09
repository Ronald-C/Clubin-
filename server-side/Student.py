# Student entity

from cerberus import Validator
import sys

from Connector import Database
from CustomException import *

class Student(Database):

	def __init__(self):
		self.conn = super(Student, self).connect()
		self.session = super(Student, self).getSession()

	def join(self, studentID, organizationName):
		try:
			# Cast to string if studentID typeof integer
			if isinstance(studentID, int):
				studentID = str(studentID)

			schema = {
				'SJSU': {
					'required': True,
					'type': 'string',
					'maxlength': 9
				},
				'OrganizationName': {
					'required': True,
					'type': 'string',
					'minlength': 3,
					'maxlength': 45
				}
			}

			v = Validator()	
			validStatus = v.validate({
					'SJSU': studentID,
					'OrganizationName': organizationName
				}, schema)

			# Validate returns False if failed to meet rules
			if not validStatus: raise ValidatorException(v.errors)

			# Check if student not already member
			self.session.execute("""
				SELECT * FROM MemberOf as mem
					WHERE mem.`Student_fk` =
						(SELECT s.`UID` FROM Student as s WHERE s.`SJSUID` = %s)
					AND mem.`Organization_fk` = 
						(SELECT o.`OrganizationID` FROM Organization as o WHERE o.`OrganizationName` = %s);
				""", (studentID, organizationName))

			data = self.session.fetchone()
			
			if not data:	# Add student to organization 
				self.session.execute("""
					INSERT INTO MemberOf (`Student_fk`, `Organization_fk`)
						VALUES (
							(SELECT s.`UID` FROM Student as s WHERE s.`SJSUID` = %s),
							(SELECT o.`OrganizationID` FROM Organization as o WHERE o.`OrganizationName` = %s)
						);
					""", (studentID, organizationName))

				self.conn.commit()

			else:	# Check if student inactive member of organization
				self.session.execute("""
				SELECT * FROM MemberOf as mem
					WHERE mem.`Student_fk` =
						(SELECT s.`UID` FROM Student as s WHERE s.`SJSUID` = %s)
					AND mem.`Organization_fk` = 
						(SELECT o.`OrganizationID` FROM Organization as o WHERE o.`OrganizationName` = %s)
					AND mem.`Active` = '0';
				""", (studentID, organizationName))

				notActive = self.session.fetchone()
				if notActive: # Update organization member active status
					self.session.execute("""
						UPDATE MemberOf
							SET MemberOf.`Active` = '1' 
							WHERE MemberOf.`Student_fk` = 
								(SELECT s.`UID` FROM Student as s WHERE s.`SJSUID` = %s);
						""", studentID)
									
					self.conn.commit()

				else:	# Organization member already active
					print "[WARNING] %s in %s already active" % (studentID, organizationName)

		except (ValidatorException, Exception) as e:
			self.conn.rollback()
			print "[WARNING] %s" % e

