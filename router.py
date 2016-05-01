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
    request, url_for, session
)

# Add directory to path to access modules outside of ./
abspath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(abspath, 'server-side'))

# View modules
from AccessControl import Registration, Authentication
from Student import Student

__builtin__.DEBUG = True                        # Global debug setting
app = Flask('Clubin')                           # Flask app
app.config['SECRET_KEY'] = 'super secret key'   # session variable

##########################################################

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

Register = Registration()
# Defined student registration processor 
@app.route('/sRegistration', methods=['GET', 'POST'])
def studentRegistration():
    """
    The return is of the form: errors = { 'SUCCESS': '', 'ERROR': '' }
    @Return:
        - Success = 1 : Indicates successful registration
        - Success = 0 : There was an error, reference ERROR key
        - False: 500 system error

    """
    if request.method == 'GET':
        return redirect(url_for('signup'))

    try:
        _studentID = request.form['SJSUID']
        _FirstName = request.form['FirstName']
        _LastName = request.form['LastName']
        _Password = request.form['Password']
        _MiddleName = request.form['MiddleName']
        _studentEmail = request.form['Email']

        # Create a student account in database.
        status = Register._addStudent(studentID=_studentID, studentEmail=_studentEmail, 
            FirstName=_FirstName, LastName=_LastName, Password=_Password, MiddleName=_MiddleName)

        if isinstance(status, dict):
            return json.dumps(status)

        else:
            return redirect('errors/500.html')

    except Exception as err:
        # Default exception handler
        return render_template('errors/500.html')         

# Render the user login page
@app.route('/login')
def login():
    return render_template('login.html')

Authenticator = Authentication()
# Defined user login processor
@app.route('/userLogin', methods=['GET', 'POST'])
def userLogin():
    if request.method == 'GET':
        return redirect(url_for('login'))

    try:
        _username = request.form['Username']
        _password = request.form['Password']

        status = Authenticator._authorize(username=_username, password=_password)
        if 'SUCCESS' in status:
            
            if status['SUCCESS'] == '1':    # OK
                return render_template('studenthome.html')

            else:           # Errors caught
                flash(status)               
                return redirect(url_for('login'))
        
        else:       # Something bad happened
            return render_template('errors/500.html')

    except Exception as e:
        # Default exception handler
        return render_template('errors/500.html') 

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

