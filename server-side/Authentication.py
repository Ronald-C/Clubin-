# Authentication helper

import traceback
from stormpath.client import Client
from os import environ, path

from Connector import Database
from Validater import Validate

# DEBUG = True

# abspath = path.dirname(path.abspath(__file__))

# # Create a new Stormpath Client.
# apiKeys = path.join(abspath, '../security/apiKey.properties')
# client = Client(api_key_file_location=apiKeys)
# href = environ['STORMPATH_APPLICATION_HREF']

# # Retrieve our application
# stormApp = client.applications.get(href)


# class Authentication(Database):
# 	"""
# 	A class that authenticates accounts for login
	
# 	"""
# 	def __init__(self):
# 		super(Authentication, self).__init__()
# 		# Get connection & cursor from Database
# 		self.conn = super(Authentication, self).connect()
# 		self.session = super(Authentication, self).getSession()

# 	