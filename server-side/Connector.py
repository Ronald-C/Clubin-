#!/usr/bin/python

# References
# 
# -	http://www.mikusa.com/python-mysql-docs/index.html
# -	http://mysql-python.sourceforge.net/mdb.html
# -	http://zetcode.com/db/mysqlpython/
# 

import MySQLdb as mdb 		# _mysql Python wrapper
import sys
import json

class Connection(object):

	__database		= None
	__instance  	= None 	
	__connection 	= None
	__session 		= None 		# Database cursor object

	def __init__(self):
		# Controls initialization of a new instance
		try:
			with open('security/config.json', 'r') as f:
				cfg = json.load(f)["mysql"]		# Access credentials
			
			self.__connect(cfg['host'], cfg['user'], cfg['passwd'], cfg['db'])	
			f.close()
		
		except IOError as e:
			print e

	## End def __init__

	def __connect(self, host='', user='', passwd='', database=''):
		if Connection.__session is not None:
			# Prevent mulitple instance of connection
			return

		Connection.__database = database

		try:
			if not Connection.__database:
				raise NameError('Unspecified database');

			conn = mdb.connect(host, user, passwd, Connection.__database)
			Connection.__connection = conn

			# Set data retrieval return type as dictionary
			Connection.__session = conn.cursor(mdb.cursors.DictCursor)

			Connection.__session.execute("SELECT VERSION()");
			ver = Connection.__session.fetchone()
			print "[SERVER] Database ver: %s " % ver

		except mdb.Error as e:
			print "Error %d: %s" % (e.args[0], e.args[1])
			sys.exit(1)

	## End def __connect

	def close(self):	
		if Connection.__session:
			Connection.__session.close()
			Connection.__connection.close()

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