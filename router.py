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
from datetime import timedelta

# Add directory to path to access modules outside of ./
abspath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(abspath, 'server-side'))

# View modules
from Helpers import login_required
from AccessControl import Registration, Authentication
from Student import Student

__builtin__.DEBUG = True                        # Global debug setting
app = Flask('Clubin')                           # Flask app
app.secret_key = os.urandom(24)                 # session variable
# app.permanent_session_lifetime = timedelta(hours=12)

Authenticator = Authentication()
Register = Registration()
student = Student()

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

####################### STUDENT VIEW #######################

# Defined user login processor
@app.route('/userLogin', methods=['GET', 'POST'])
def userLogin():
    if request.method == 'GET':
        return redirect(url_for('login'))

    try:
        _username = request.form['Username']
        _password = request.form['Password']
        status = Authenticator._authorize(username=_username, password=_password)
        if isinstance(status, dict):

            if status['SUCCESS'] == '1':    # OK
                studentInfo = student.getStudentInfo(_username)

                if studentInfo == False:        # Fetch student info session
                    status['SUCCESS'] = '0'
                    status['ERROR'] = "Failed to find student info"

                    flash(status)       
                    return redirect(url_for('login'))
                
                else:   # Successful fetch of student info
                    session['logged_in'] = True
                    session['Info'] = dict(studentInfo)

                return redirect(url_for('studenthome'))

            else:           # Errors caught
                flash(status)               
                return redirect(url_for('login'))
        
        else:       # Something bad happened
            return render_template('errors/500.html')

    except Exception as e:
        # Default exception handler
        return render_template('errors/500.html') 

@app.route('/studenthome')
@login_required
def studenthome():
    return render_template('studenthome.html')

@app.route('/studentBulletins/<organization_id>')
@login_required
def studentBulletins(organization_id):
    a =  student.getOrganizationInfo(organization_id, session['Info']['Student']['SJSUID'])
    if a == False:
        render_template('errors/500.html')

    articles = student.getArticles(organization_id)
    comments = student.getComments(organization_id)

    if articles == False:
        articles = []

    if comments == False:
        comments = []

    return render_template('studentBulletins.html', organizationData=a, articles=articles, comments=comments)

@app.route('/studentBulletins/comment/<organization_id>', methods=['GET', 'POST'])
@login_required
def commentOnArticle(organization_id):
    status = {'SUCCESS': '0'}

    if request.method == 'GET':
        return json.dumps(status);

    try:
        sjsuid = session['Info']['Student']['SJSUID']
        success = student.commentArticle(sjsuid, request.form['studentComment'], request.form['articleID'])

        if success:     # Added comment
            status['SUCCESS'] = '1'
        
        return json.dumps(status);

    except Exception as e:
        return json.dumps(status);


@app.route('/interests')
@login_required
def interests():
    """ 
    NOTE: Really returning all interests not associated with student. 
    """
    ints = student.getAllInterests(session['Info']['Student']['UID'])
    return render_template('interests.html', interest=ints)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/search')
@login_required
def search():
    return render_template('search.html')


####################### ORGANIZATION VIEW #######################

@app.route('/orgprofile')
def orgprofile():
    return render_template('orgprofile.html')

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


@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash("You have been logged out!")
    return redirect(url_for('index'))
        

# Default catch all routes
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return redirect(url_for('studenthome'))


if __name__ == '__main__':
    DEFAULT_HOST = '127.0.0.1'      # Set env to config host/port
    DEFAULT_PORT = 5000

    if 'PORT' in os.environ:
        DEFAULT_PORT = int(os.environ['PORT'])

    if 'HOST' in os.environ:
        DEFAULT_HOST = str(os.environ['HOST'])

    app.run(host=DEFAULT_HOST, port=DEFAULT_PORT, debug=DEBUG)

