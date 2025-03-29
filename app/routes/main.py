from flask import Blueprint, request, render_template, redirect, url_for

main = Blueprint("main", __name__)

@main.route("/")
def landing_page():
    return render_template("index.html")