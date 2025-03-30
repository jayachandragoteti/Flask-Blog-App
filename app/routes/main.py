from flask import Blueprint, request, render_template, redirect, url_for

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

@main.route("/profile")
def profile():
    return render_template("index.html")