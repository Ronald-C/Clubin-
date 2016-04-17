#Advisor
from Connector import Database
class Advisor(Database)
    def __init__(advisors):
        advisors.conn = super(Advisor, advisors).connect()
        advisors.session = super(Advisor, advisors).getSession()
    
    def addAdvisor(advisors, AdvisorID, FirstName, MiddleName=None, LastName, Email, Department):
        advisors.session.execute("INSERT INTO 'Clubin'. 'Advisor' ('AdvisorID', 'FirstName','MiddleName','LastName','Email','Department')       VALUES(%s,%s,%s,%s,%s)", (AdvisorID, FirstName, MiddleName, LastName, Email, Department))
        advisors.conn.commit()
    def editAdvisor():
        pass
db = Advisor()
db.addAdvisor("", "", "", "", "", "")