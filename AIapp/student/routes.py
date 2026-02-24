from flask import Blueprint, render_template, session, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["tpo_portal"]

users_collection = db["users"]
students_col = db["students"]   # <-- required for profile view

# Blueprint
student_bp = Blueprint("student", __name__, url_prefix="/student")


# ---------------- LOGIN CHECK HELPER ----------------
def require_login():
    if "user_email" not in session:
        return redirect(url_for("auth.index"))
    return None


# ---------------- DASHBOARD ----------------
@student_bp.route("/dashboard")
def dashboard():

    check = require_login()
    if check:
        return check

    user = users_collection.find_one({"email": session["user_email"]})

    if not user:
        session.clear()
        return redirect(url_for("auth.index"))

    return render_template(
        "STUDENT.html",
        name=user.get("fullname", "Student"),
        branch=user.get("branch", "B.Tech AI"),
        enrollment=user.get("enrollment", "N/A"),
        points=user.get("points", 0)
    )


# ---------------- CHATBOT ----------------
@student_bp.route("/chatbot")
def chatbot():
    check = require_login()
    if check:
        return check
    return render_template("chatbot.html")


# ---------------- AI PREDICTION ----------------
@student_bp.route("/prediction")
def prediction():
    check = require_login()
    if check:
        return check
    return render_template("predict.html")


# ---------------- MOCK INTERVIEW ----------------
@student_bp.route("/mock")
def mock():
    check = require_login()
    if check:
        return check
    return render_template("mock.html")


# ---------------- JOB LIST PAGE ----------------
@student_bp.route("/jobs")
def jobs():
    check = require_login()
    if check:
        return check
    return render_template("job.html")


# ---------------- VIEW STUDENT PROFILE ----------------
@student_bp.route("/profile/<id>", methods=["GET"])
def view_student(id):
    if "user_email" not in session:
        return redirect(url_for("auth.index"))

    student = users_collection.find_one({"_id": ObjectId(id)})
    if not student:
        return "Student Not Found", 404

    return render_template("student_profile.html", student=student)

@student_bp.route("/logout")
def logout():
    session.clear()   # 👈 saari session values remove
    return redirect(url_for("auth.index"))

