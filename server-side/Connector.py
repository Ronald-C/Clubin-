#!/usr/bin/python

# http://www.tutorialspoint.com/python/python_database_access.htm
# http://mysql-python.sourceforge.net/mdb.html
# http://zetcode.com/db/mysqlpython/
# http://www.mysqltutorial.org/python-connecting-mysql-databases/

import MySQLdb as mdb 		# _mysql Python wrapper
import sys
import json

class Connection:

	__database		= None
	__instance 		= None 	
	__connection 	= None
	__session 		= None 		# Database cursor object

	def __new__(cls, *args, **kwargs):
		if not cls.__instance and not cls.__database:
			cls.__instance = super(Connection, cls).__new__(cls, *args, **kwargs)
		else:
			return cls.__instance
	## End def __new__

	def __init__(self):
		try:
			with open('security/config.json', 'r') as f:
				cfg = json.load(f)["mysql"]		# Access credentials
			self.__connect(cfg['host'], cfg['user'], cfg['passwd'], cfg['db'])
			f.close()
		except IOError as e:
			print e
	## End def __init__

	def __connect(self, host='', user='', passwd='', database=''):
		self.__database = database
		try:
			conn = mdb.connect(host, user, passwd, self.__database)
			self.__connection = conn
			# Set data retrieval return type as dictionary
			self.__session = conn.cursor(mdb.cursors.DictCursor)

			self.__session.execute("SELECT VERSION()");
			ver = self.__session.fetchone()
			print "[SERVER] Database ver: %s " % ver

		except mdb.Error as e:
			print "Error %d: %s" % (e.args[0], e.args[1])
			sys.exit(1)
	## End def __connect

	def close(self):	
		if self.__session:
			self.__session.close()
			self.__connection.close()
	## End def close

def main():
	try:
		tx = Connection()
		print "[Server] Test connection success"
		tx.close()
	except Exception, e:
		print e
		sys.exit(1)

if __name__ == '__main__':
	main()