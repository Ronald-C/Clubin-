#!/usr/bin/python

# References
# 
# -	http://www.mikusa.com/python-mysql-docs/index.html
# -	http://mysql-python.sourceforge.net/mdb.html
# -	http://zetcode.com/db/mysqlpython/
# - https://www.python.org/dev/peps/pep-0249/
#

import MySQLdb as mdb 		# _mysql Python wrapper
import sys
from json import load

class Database(object):

	__database		= None	
	__connection 	= None
	__session 		= None 		# Database cursor object

	def __init__(self):
		# Controls initialization of a new instance
		pass

	@classmethod
	def connect(cls):
		try:
			with open('security/config.json', 'r') as f:
				cfg = load(f)["mysql"]		# Access credentials
			
			cls.__connect(cfg['host'], cfg['user'], cfg['passwd'], cfg['db'])	
			f.close()

			return cls.__connection 	# Return conn instance
		
		except IOError as e:
			print "[ERROR] %s" % e

	@classmethod
	def getSession(cls):
		return cls.__session

	@classmethod
	def __connect(cls, host='', user='', passwd='', database=''):
		if cls.__session is not None:
			# Prevent mulitple instance of connection
			return 

		cls.__database = database

		try:
			if not cls.__database:
				raise NameError('Unspecified database');

			conn = mdb.connect(host, user, passwd, cls.__database)
			cls.__connection = conn

			# Ensure autocommit disabled == Default
			cls.__connection.autocommit(False)

			# Set data retrieval return type as dictionary
			cls.__session = conn.cursor(mdb.cursors.DictCursor)

			cls.__session.execute("SELECT VERSION()");
			ver = cls.__session.fetchone()
			print "[SERVER] Database ver: %s " % ver

		except mdb.Error as e:
			print "[ERROR] %d: %s" % (e.args[0], e.args[1])
			sys.exit(2)

		except Exception as e:
			print "[ERROR] %s" % e
			sys.exit(1)


	@classmethod
	def close(cls):	
		if cls.__session:
			cls.__session.close()
			cls.__connection.close()

def main():
	try:
		tx = Database()
		tx.connect()
		print "[SERVER] Test connection success"
		tx.close()

	except Exception, e:
		print "[ERROR] %s" % e
		sys.exit(1)


if __name__ == '__main__':
	main()