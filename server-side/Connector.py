#!/usr/bin/python

# References
# 
# -	http://www.mikusa.com/python-mysql-docs/index.html
# -	http://mysql-python.sourceforge.net/mdb.html
# -	http://zetcode.com/db/mysqlpython/
# - https://www.python.org/dev/peps/pep-0249/
#

import MySQLdb as mdb 		# _mysql Python wrapper
from sys import exit
from json import load

#from flask import Flask
#app = Flask(__name__)
#@app.route('/')
#def home():
#    return "Hey there!"
#if __name__ == '__main__':
#    app.run(debug=True)

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
			print e

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

			# Set data retrieval return type as dictionary
			cls.__session = conn.cursor(mdb.cursors.DictCursor)

			cls.__session.execute("SELECT VERSION()");
			ver = cls.__session.fetchone()
			print "[SERVER] Database ver: %s " % ver

		except mdb.Error as e:
			print "Error %d: %s" % (e.args[0], e.args[1])
			exit(1)


	@classmethod
	def close(cls):	
		if cls.__session:
			cls.__session.close()
			cls.__connection.close()

def main():
	try:
		tx = Database()
		print "[Server] Test connection success"
		tx.close()
	except Exception, e:
		print e
		sys.exit(1)


if __name__ == '__main__':
	main()