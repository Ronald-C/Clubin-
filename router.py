from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/widgets')
def widgets():
    return render_template('widgets.html')

@app.route('/interests')
def interests():
    return render_template('interests.html')

@app.route('/hometemplate')
def hometemplate():
    return render_template('hometemplate.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

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

@app.route('/clubs', methods=['POST'])
def clubs():
    fname=request.form['fname']
    mname=request.form['mname']
    lname=request.form['lname']
    sid=request.form['sid']
    email=request.form['email']
    password=request.form['password']
    return render_template('clubs.html', fname=fname, mname=mname, lname=lname, sid=sid, email=email, pasword=password)

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


if __name__ == '__main__':
    app.run(debug=True)