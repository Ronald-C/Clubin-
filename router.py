# 
# REFERENCES
# - http://flask.pocoo.org/docs/0.10/api/
# - http://flask.pocoo.org/docs/0.10/quickstart/#routing

import os
import sys
import __builtin__
import json
from flask import (
    Flask, abort, flash, redirect, render_template,
    request, url_for,
)
from stormpath.client import Client

# Add directory to path to access modules outside of ./
abspath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(abspath, 'server-side'))

# View modules
from Registration import Registration
from Student import Student

__builtin__.DEBUG = True
app = Flask('Clubin')      # Flask app

# Create a new Stormpath Client.
apiKeys = os.path.join(abspath, 'security/apiKey.properties')
client = Client(api_key_file_location=os.path.expanduser(apiKeys))
# Retrieve our application
href = 'https://api.stormpath.com/v1/applications/77J8SNb4s5dMV8eJQ4Ujw1'
stormApp = client.applications.get(href)

# Defined landing page
@app.route('/')
def index():
    return render_template("index.html")

# Render the registration HTML page
@app.route('/signup')
def signup():
    return render_template('signup.html')
    
# Defined organization registration processor
@app.route('/oRegistration', methods=['GET', 'POST'])
def organizationRegistration():
    pass

# Defined student registration processor 
Register = Registration()
asd = Registration()
@app.route('/sRegistration', methods=['GET', 'POST'])
def studentRegistration():
    if request.method == 'GET':
        return render_template(url_for('signup'))

    errors = { 'SUCCESS': '', 'ERROR': '' }     # status return
    # print request.form
    
    try:
        _studentID = request.form['SJSUID']
        _FirstName = request.form['FirstName']
        _LastName = request.form['LastName']
        _Password = request.form['Password']
        _MiddleName = request.form['MiddleName']
        _studentEmail = request.form['Email']

        # Query stormpath if user exists
        stormAccount = stormApp.accounts.search({
            'email': _studentEmail
        })        

        if len(stormAccount) == 1:       # Account exists
            errors['SUCCESS'] = '0'
            errors['ERROR'] = 'Please verify inputs'

            return json.dumps(errors)

        try:
            # Check if user exists in database
            isUser = Register.existingUser(email=_studentEmail)
            
            if isUser:                  # Account exists
                raise Exception("Please verify inputs")

            else: 
                # Validate user information is correct for database
                Register._validate(studentID=_studentID, studentEmail=_studentEmail, 
                    FirstName=_FirstName, LastName=_LastName, MiddleName=_MiddleName)

                # Create a new Stormpath Account.
                account = stormApp.accounts.create({
                    'given_name': _FirstName,
                    'middle_name': _MiddleName,
                    'surname': _LastName,
                    'email': _studentEmail,
                    'password': _Password
                })

        except Exception as e:     # Stormpath requirements not met
            errors['SUCCESS'] = '0'
            errors['ERROR'] = str(e)

            return json.dumps(errors)

        # print account.email

        # Create a student account in database.
        status = Register._addStudent(studentID=_studentID, studentEmail=_studentEmail, 
            FirstName=_FirstName, LastName=_LastName, MiddleName=_MiddleName)
            
        if status == True:
            errors['SUCCESS'] = '1'

        elif isinstance(status, dict):
            errors['SUCCESS'] = '0'
            errors['ERROR'] = status


        return json.dumps(errors)

    except Exception as err:
        # Uncaught exception, return to register page
        return         



@app.route('/orgprofile')
def orgprofile():
    return render_template('orgprofile.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/widgets')
def widgets():
    return render_template('widgets.html')

@app.route('/studentsignup')
def studentsignup():
    return render_template('studentsignup.html')


@app.route('/studenttemplate')
def studenttemplate():
    return render_template('studenttemplate.html')

@app.route('/studenthome')
def studenthome():
    return render_template('studenthome.html')

@app.route('/orgsignup')
def orgsignup():
    return render_template('orgsignup.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/interests')
def interests():
    return render_template('interests.html')

@app.route('/orgsettings')
def orgsettings():
    return render_template('orgsettings.html')

@app.route('/clubs', methods=['POST'])
def clubs():
    fname=request.form['fname']
    mname=request.form['mname']
    lname=request.form['lname']
    sid=request.form['sid']
    email=request.form['email']
    password=request.form['password']
    return render_template('clubs.html', fname=fname, mname=mname, lname=lname, sid=sid, email=email, pasword=password)

@app.route('/org')
def org():
    return render_template('orghome.html')

@app.route('/orghome', methods=['POST'])
def orghome():
    org=request.form['org']
    aFname=request.form['aFname']
    aLname=request.form['aLname']
    aid=request.form['aid']
    aemail=request.form['aemail']
    dept=request.form['dept']
    orgemail=request.form['orgemail']
    password=request.form['password']
    return render_template('orghome.html', org=org, aFname=aFname, aLname=aLname, aid=aid, aemail=aemail, dept=dept, orgemail=orgemail, password=password)

#
#@app.route('/buttons')
#def buttons():
#    return render_template('buttons.html')


# Default catch all routes; 401 status
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return 'You want path: %s' % path


if __name__ == '__main__':
    DEFAULT_HOST = '127.0.0.1'      # Set env to config host/port
    DEFAULT_PORT = 5000

    if 'PORT' in os.environ:
        DEFAULT_PORT = int(os.environ['PORT'])

    if 'HOST' in os.environ:
        DEFAULT_HOST = str(os.environ['HOST'])

    app.run(host=DEFAULT_HOST, port=DEFAULT_PORT)
