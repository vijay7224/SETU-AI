from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import users
from flask import session


auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/")
def index():
    return render_template("HOME.html")

@auth_bp.route("/login", methods=["POST","GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    email = request.form.get("email")
    password = request.form.get("password")
    role = request.form.get("role")

    user = users.find_one({"email": email, "role": role})

    if not user:
        flash("User not found!", "danger")
        return redirect(url_for("auth.index"))

    if not check_password_hash(user["password"], password):
        flash("Invalid password!", "danger")
        return redirect(url_for("auth.index"))

    if role == "student" and not user.get("approved", False):
        flash("TPO approval pending!", "warning")
        return redirect(url_for("auth.index"))
    session["user_email"] = user["email"]
    session["user_id"] = str(user["_id"])

    if role == "student":
        return redirect(url_for("student.dashboard"))
    elif role == "tpo":
        return redirect(url_for("tpo.welcome"))
    elif role == "hr":
        return redirect(url_for("hr.welcome"))

@auth_bp.route("/register", methods=["POST"])
def register():
    fullname = request.form.get("fullname")
    email = request.form.get("email")
    password = request.form.get("password")
    enrollment = request.form.get("enrollment")

    if users.find_one({"email": email}):
        flash("Email already registered!", "danger")
        return redirect(url_for("auth.index"))

    users.insert_one({
        "fullname": fullname,
        "email": email,
        "password": generate_password_hash(password),
        "role": "student",
        "enrollment": enrollment,
        "approved": True
    })

    flash("Registration successful! Login now.", "success")
    return redirect(url_for("auth.index"))
