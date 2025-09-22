from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.student import Student
from werkzeug.security import generate_password_hash
import traceback

student_bp = Blueprint("student", __name__, url_prefix="")

@student_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            print(f"Received registration data: {name}, {email}")  # Debug print

            s = Student()
            success = s.register(name, email, password)

            if success:
                flash("Registration successful! Please login.", "success")
                return redirect(url_for("student.login"))
            else:
                flash("Registration failed.", "danger")
        except Exception as e:
            print(f"Error during registration: {e}")
            traceback.print_exc()
            flash(f"Registration failed: {str(e)}", "danger")
    return render_template("register.html")
   

@student_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            s = Student()
            user = s.login(email, password)
            session["student_id"] = user["student_id"]
            session["student_name"] = user["name"]
            flash("Logged in successfully.")
            return redirect(url_for("student.submit_feedback_view"))
        except AuthenticationError as e:
            flash(str(e))
            return render_template("login.html")
        except Exception as e:
            flash("Login error: " + str(e))
            return render_template("login.html")
    return render_template("login.html")

@student_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out.")
    return redirect(url_for("student.login"))

@student_bp.route("/submit_feedback", methods=["GET", "POST"])
def submit_feedback_view():
    if "student_id" not in session:
        flash("Please login first.")
        return redirect(url_for("student.login"))
    s = Student()
    if request.method == "POST":
        course_id = request.form.get("course_id")
        rating = int(request.form.get("rating"))
        comments = request.form.get("comments")
        try:
            s.submit_feedback(session["student_id"], course_id, rating, comments)
            flash("Feedback submitted. Thank you.")
            return redirect(url_for("student.submit_feedback_view"))
        except DuplicateFeedbackError as e:
            flash(str(e))
        except Exception as e:
            flash("Error submitting feedback: " + str(e))
    courses = s.get_courses()
    return render_template("submit_feedback.html", courses=courses)

@student_bp.route("/download_logs")
def download_logs():
    log_path = current_app.config.get("LOG_FILE")
    if not os.path.exists(log_path):
        flash("Log file not found.")
        return redirect(url_for("student.submit_feedback_view"))
   # return send_file(log_path, as_attachment=True)
    return render_template("login.html", courses=courses)
