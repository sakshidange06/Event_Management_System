from functools import wraps
from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

import storage

app = Flask(__name__)
app.secret_key ="change-this-to-any-random-text"

CATEGORIES = ["Conference", "Workshop", "Seminar", "Cultural", "Sports",
              "Wedding", "Party", "Other"]


def event_from_form():
    return {
        "title": request.form["title"].strip(),
        "category": request.form["category"],
        "date": request.form["date"],
        "time": request.form["time"],
        "venue": request.form["venue"].strip(),
        "organizer": request.form["organizer"].strip(),
        "capacity": int(request.form.get("capacity") or 0),
        "description": request.form.get("description", "").strip(),
    }

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
    return redirect(url_for("events"))

@app.route("/events")
@login_required
def events():
    q = request.args.get("q", "").strip().lower()
    category = request.args.get("category", "")

    rows = storage.all_rows("Events")
    if q:
        rows = [e for e in rows if q in " ".join(
            str(e[k]) for k in ("title", "venue", "organizer", "category")).lower()]
    if category:
        rows = [e for e in rows if e["category"] == category]
    rows.sort(key=lambda e: (e["date"], e["time"]))

    return render_template("events.html", events=rows, q=q,
                           selected=category, categories=CATEGORIES)


@app.route("/events/add", methods=["GET", "POST"])
@login_required
def add_event():
    if request.method == "POST":
        data = event_from_form()
        data["created_by"] = session["user_name"]
        storage.add_row("Events", data)
        flash("Event added successfully.", "success")
        return redirect(url_for("events"))
    return render_template("event_form.html", event=None, categories=CATEGORIES)


@app.route("/events/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_event(id):
    event = storage.get_row("Events", id)
    if not event:
        flash("Event not found.", "danger")
        return redirect(url_for("events"))

    if request.method == "POST":
        storage.update_row("Events", id, event_from_form())
        flash("Event updated.", "success")
        return redirect(url_for("events"))
    return render_template("event_form.html", event=event, categories=CATEGORIES)


@app.route("/events/<int:id>/delete", methods=["POST"])
@login_required
def delete_event(id):
    storage.delete_row("Events", id)
    flash("Event deleted.", "info")
    return redirect(url_for("events"))

if __name__ == "__main__":
    app.run(debug=True)