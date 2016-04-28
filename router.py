from datetime import datetime

from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from flask.ext.stormpath import (
    StormpathError,
    StormpathManager,
    User,
    login_required,
    login_user,
    logout_user,
    user,
)

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'some_really_long_random_string_here'
app.config['STORMPATH_API_KEY_FILE'] = 'apiKey.properties'
app.config['STORMPATH_APPLICATION'] = 'flaskr'

stormpath_manager = StormpathManager(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/')
def dashboard():
    posts = []
    for account in stormpath_manager.application.accounts:
        if account.custom_data.get('posts'):
            posts.extend(account.custom_data['posts'])

    posts = sorted(posts, key=lambda k: k['date'], reverse=True)
    return render_template('profile.html', posts=posts)


@app.route('/add', methods=['POST'])
@login_required
def add_post():
    if not user.custom_data.get('posts'):
        user.custom_data['posts'] = []

    user.custom_data['posts'].append({
        'date': datetime.utcnow().isoformat(),
        'title': request.form['title'],
        'text': request.form['text'],
    })
    user.save()

    flash('New post successfully added.')
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    logout_user()
    flash('You were logged out.')
    return redirect(url_for('dashboard'))




@app.route('/orgprofile')
def orgprofile():
    return render_template('orgprofile.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/widgets')
def widgets():
    return render_template('widgets.html')

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


if __name__ == '__main__':
    app.run(debug=True)