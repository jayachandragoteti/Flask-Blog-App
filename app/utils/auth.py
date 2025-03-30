from flask import session, redirect, url_for, flash
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("login_user"):
            flash("You need to log in to access this page.", "warning")
            return redirect(url_for("auth.login_user"))
        return f(*args, **kwargs)
    return decorated_function
