

import os
from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from app.utils import login_required 
from app.models import Users
from app.extensions import db
from datetime import datetime

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/about")
def about():
    return render_template("index.html")


@main.route("/contact")
def contact():
    return render_template("index.html")

@main.route("/dashboard")
def dashboard():
    return render_template("index.html")



# Allowed image extensions
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
# Define the upload folder path
UPLOAD_FOLDER = os.path.join(os.getcwd(), "app/static/images/uploads")
if not os.path.exists(UPLOAD_FOLDER):  # Create if it doesn't exist
    os.makedirs(UPLOAD_FOLDER)
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user_session_data = session.get("login_user")

    if not user_session_data:
        flash("You need to log in to access this page.", "warning")
        return redirect(url_for("auth.logout"))

    # Fetch the current user from the database
    current_user = Users.query.filter_by(
        id=user_session_data.get("user_id"),
        email=user_session_data.get("email")
    ).first()

    if not current_user:
        flash("User not found. Please log in again.", "danger")
        return redirect(url_for("auth.logout"))

    # Handle form submission
    if request.method == "POST":
        email = request.form.get("email","")
        full_name = request.form.get("full_name",)
        phone_number = request.form.get("phone_number")
        dob_str = request.form.get("dob")
        gender = request.form.get("gender")
        address = request.form.get("address")

        # Handle profile picture upload
        if "profile_picture" in request.files:
            file = request.files["profile_picture"]
            if file and allowed_file(file.filename):
                # Generate a unique filename using user ID
                filename = f"avatar_user_{current_user.id}.jpg"
                file_path = os.path.join(UPLOAD_FOLDER, filename)

                # Save the file
                file.save(file_path)

                # Update the user's profile picture field in the database
                current_user.profile_picture = filename
            elif file.filename:  # If file exists but not allowed
                flash("Invalid file format. Please upload a PNG or JPG image.", "danger")

        # Convert DOB string to a Python date object
        if dob_str:
            try:
                dob = datetime.strptime(dob_str, "%Y-%m-%d").date()  # Convert to date object
            except ValueError:
                flash("Invalid date format! Please use YYYY-MM-DD.", "danger")
                return redirect(url_for("main.profile"))
        else:
            dob = None
        
        # Update user fields if values are provided
        current_user.email = email if email else current_user.email
        current_user.full_name = full_name if full_name else current_user.full_name
        current_user.phone_number = phone_number if phone_number else current_user.phone_number
        current_user.dob = dob if dob else current_user.dob  # Save as date object
        current_user.gender = gender if gender else current_user.gender
        current_user.address = address if address else current_user.address

        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for("main.profile"))

    return render_template("profile.html", user=current_user)
