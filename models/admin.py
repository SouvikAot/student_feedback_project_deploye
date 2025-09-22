from models.database import DatabaseConnection
from models.logger import write_log
from models.exceptions import AuthenticationError
from werkzeug.security import check_password_hash

class Admin:  # ✅ This must be exactly like this
    def __init__(self):
        self.db = DatabaseConnection()

    def login(self, username, password):
        try:
            self.db.connect()
            query = "SELECT * FROM admins WHERE username=%s"
            cur = self.db.execute(query, (username,))
            row = cur.fetchone()
            if row and check_password_hash(row.get("password"), password):
                write_log(f"Admin login successful username={username}")
                return row
            else:
                write_log(f"Admin login failed username={username}", level="warning")
                raise AuthenticationError("Invalid username/password")
        finally:
            self.db.disconnect()

    def view_all_feedback(self):
        try:
            self.db.connect()
            q = """
            SELECT f.feedback_id, s.name as student_name, s.email as student_email,
                   c.course_name, c.faculty_name, f.rating, f.comments, f.created_at
            FROM feedback f
            JOIN students s ON f.student_id = s.student_id
            JOIN courses c ON f.course_id = c.course_id
            ORDER BY f.created_at DESC
            """
            cur = self.db.execute(q)
            return cur.fetchall()
        finally:
            self.db.disconnect()
