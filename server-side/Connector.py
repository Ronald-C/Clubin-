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
	""" MySQL database connection class

	Handles all connection/cursor instances to database. As a minimal project, class
	only instances a single shared connection. Implementing pooled connections is possible
	by refactoring this class a minimal impact to other modules that require Database class
	"""

	__database		= None	
	__connection 	= None
	__session 		= None 		# Database cursor object

	def __init__(self):
		# Controls initialization of a new instance
		pass

	@classmethod
	def connect(cls):
		if cls.__session is not None:
			# Prevent mulitple instance of connection
			return 
		
		try:
			with open('security/config.json', 'r') as f:
				cfg = load(f)["mysql"]		# Access credentials
				cls.configFile = f 		# Save file instance
			
			cls.__database = cfg['db']
			if not cls.__database:	# Check if empty string DB
				raise NameError('Unspecified database');

			conn = cls.__connect(cfg['host'], cfg['user'], cfg['passwd'], cfg['db'])	
			cls.__connection = conn

			# Set data retrieval return type as dictionary
			cls.__session = conn.cursor(mdb.cursors.DictCursor)

			cls.__session.execute("SELECT VERSION()");
			ver = cls.__session.fetchone()
			print "[SERVER] Database ver: %s " % ver

			return cls.__connection 	# Return conn instance

		except mdb.Error as e:
			print "[ERROR] %d: %s" % (e.args[0], e.args[1])
			sys.exit(2)
		
		except Exception as e:
			print "[ERROR] %s" % e
			sys.exit(1)

		finally:
			# Close file even if exception raised
			cls.configFile.close()	

	@classmethod
	def getSession(cls):
		return cls.__session

	@staticmethod
	def __connect(host, user, passwd, database):
		try:
			conn = mdb.connect(host, user, passwd, database)

			# Ensure autocommit disabled == Default
			conn.autocommit(False)

			return conn

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