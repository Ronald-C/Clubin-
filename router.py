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

@app.route('/topnav')
def topnav():
    return render_template('top-nav.html')

if __name__ == '__main__':
    app.run(debug=True)