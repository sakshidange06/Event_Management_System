from functools import wraps
from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

import storage

app = Flask(__name__)
app.secret_key = "change-this-to-any-random-text"


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in first.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        if any(u["email"] == email for u in storage.all_rows("Users")):
            flash("This email is already registered.", "danger")
        else:
            storage.add_row("Users", {
                "name": name,
                "email": email,
                "password": generate_password_hash(password),
            })
            flash("Registration successful. Please log in.", "success")
            return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        user = next((u for u in storage.all_rows("Users") if u["email"] == email), None)

        if user and check_password_hash(user["password"], request.form["password"]):
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            return redirect(url_for("home"))
        flash("Invalid email or password.", "danger")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


@app.route("/")
@login_required
def home():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)