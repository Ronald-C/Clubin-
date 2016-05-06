# Flask helper functions

from functools import wraps
from flask import session, redirect, url_for

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
			return f(*args, **kwargs)
        else:
			return redirect(url_for('index'))

    return wrap