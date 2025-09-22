from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, send_file
from models.admin import Admin
from models.logger import write_log
from models.exceptions import AuthenticationError
import os

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# -----------------------
# Admin Login
# -----------------------
@admin_bp.route("/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        adm = Admin()
        try:
            user = adm.login(username, password)
            session["admin_id"] = user["admin_id"]
            session["admin_username"] = user["username"]
            flash("Admin logged in successfully.", "success")
            return redirect(url_for("admin.view_feedback"))
        except AuthenticationError as e:
            flash(str(e), "danger")
        except Exception as e:
            flash("Unexpected error: " + str(e), "danger")

    return render_template("admin_login.html")  # ✅ No "admin/" prefix

# -----------------------
# Admin Logout
# -----------------------
@admin_bp.route("/logout")
def admin_logout():
    session.pop("admin_id", None)
    session.pop("admin_username", None)
    flash("Admin logged out.", "info")
    return redirect(url_for("admin.admin_login"))

# -----------------------
# View Feedback
# -----------------------
@admin_bp.route("/view_feedback")
def view_feedback():
    if "admin_id" not in session:
        flash("Please login as admin to access this page.", "warning")
        return redirect(url_for("admin.admin_login"))

    adm = Admin()
    feedbacks = adm.view_all_feedback()

    return render_template("view_feedback.html", feedbacks=feedbacks)  # ✅ Matches your templates/

# -----------------------
# Download Logs
# -----------------------
@admin_bp.route("/download_logs")
def download_logs():
    if "admin_id" not in session:
        flash("Login required to download logs.", "warning")
        return redirect(url_for("admin.admin_login"))

    log_path = current_app.config.get("LOG_FILE")
    if not log_path or not os.path.exists(log_path):
        flash("Log file not found.", "danger")
        return redirect(url_for("admin.view_feedback"))

    return send_file(log_path, as_attachment=True)
