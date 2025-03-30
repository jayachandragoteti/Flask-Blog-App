from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from app.models import Users
from app.extensions import db 
from datetime import datetime
auth = Blueprint("auth", __name__)

@auth.route("/register", methods=["POST", "GET"])
def register_user():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if not email or not password:
            flash("All fields are required!", "danger")
            return redirect(url_for("auth.register_user"))
        # Check if user already exists
        existing_user = Users.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered. Please log in.", "warning")
            return redirect(url_for("auth.login_user"))
        
        new_user = Users(email=email)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("auth.login_user"))

    return render_template("register.html")

@auth.route("/login", methods=["POST", "GET"])
def login_user():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if not email or not password:
            flash("All fields are required!", "danger")
            return redirect(url_for("auth.login_user"))
        
        check_user = Users.query.filter_by(email=email).first() 

        if not check_user:
            flash("No account found with this email. Please register.", "warning")
            return redirect(url_for("auth.register_user"))

        if not check_user.check_password(password):
            flash("Incorrect password. Please try again.", "danger")
            return redirect(url_for("auth.login_user"))
        
        # Store user session after successful login
        session["login_user"] = {
            "user_id": check_user.id,
            "email": check_user.email,
            "current_timestamp": datetime.utcnow().isoformat()
        }
        if not session.get('login_user'):
            flash("Incorrect password. Please try again.", "danger")
            return redirect(url_for("auth.login_user"))
        
        return redirect(url_for("main.index"))
    return render_template("login.html")

@auth.route("/logout")
def logout():
    if session.get("login_user"):
        session.pop("login_user", None)
        flash("You have been logged out successfully.", "info")
    return redirect(url_for("auth.login_user"))