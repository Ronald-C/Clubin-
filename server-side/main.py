#!/usr/bin/python
from Connector import Database
class Student(Database):
    def __init__(students): # _init_ inititializing
        students.conn = super(Student, students).connect()
        students.session = super(Student, students).getSession()
        
    def addStudent(students, SJSUID, Email, FirstName, LastName, MiddleName=None):
        students.session.execute("INSERT INTO `Clubin`.`Student` (`SJSUID`, `Email`,`FirstName`, `MiddleName`, \
            `LastName`) VALUES (%s, %s, %s, %s, %s)", (SJSUID, Email, FirstName, MiddleName, LastName) ) 
        students.conn.commit()
    def editStudent():
        pass
db = Student()
db.addStudent("008288137", "reyes.joannamarie@gamil.com", "Jo-Anna Marie", "Reyes", "Rojas")