from flask import redirect, render_template, request, flash, send_file, session
from flask_app import app


@app.route("/home")
def home():
    return render_template("home.html")