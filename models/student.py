from models.database import DatabaseConnection
from werkzeug.security import generate_password_hash, check_password_hash
from models.logger import write_log
from models.exceptions import AuthenticationError, DuplicateFeedbackError
import traceback

class Student:
    def __init__(self):
        self.db = DatabaseConnection()

    def register(self, name, email, password):
        hashed = generate_password_hash(password)
        try:
            self.db.connect()
            query = "INSERT INTO students (name, email, password) VALUES (%s, %s, %s)"
            self.db.execute(query, (name, email, hashed))
            self.db.commit()  # ✅ Fixed by implementing commit in DatabaseConnection
            write_log(f"Registration successful for email={email}")
            return True
        except Exception as e:
            write_log(f"Registration failed for email={email}: {e}", level="error")
            raise
        finally:
            self.db.disconnect()

    def login(self, email, password):
        try:
            self.db.connect()
            query = "SELECT * FROM students WHERE email=%s"
            cur = self.db.execute(query, (email,))
            row = cur.fetchone()
            if row and check_password_hash(row['password'], password):
                write_log(f"Student login successful email={email}")
                return row
            else:
                write_log(f"Student login failed for email={email}", level="warning")
                raise AuthenticationError("Invalid email or password")
        except AuthenticationError:
            raise
        except Exception as e:
            write_log(f"Error during student login for {email}: {e}", level="error")
            raise
        finally:
            self.db.disconnect()

    def submit_feedback(self, student_id, course_id, rating, comments):
        try:
            self.db.connect()
            # Check for existing feedback
            check_query = "SELECT * FROM feedback WHERE student_id=%s AND course_id=%s"
            cur = self.db.execute(check_query, (student_id, course_id))
            if cur.fetchone():
                write_log(f"Duplicate feedback by student_id={student_id} for course_id={course_id}", level="warning")
                raise DuplicateFeedbackError("Feedback already submitted for this course.")

            # Insert new feedback
            insert_query = "INSERT INTO feedback (student_id, course_id, rating, comments) VALUES (%s, %s, %s, %s)"
            self.db.execute(insert_query, (student_id, course_id, rating, comments))
            self.db.commit()
            write_log(f"Feedback submitted by student_id={student_id} for course_id={course_id}")
            return True
        except Exception:
            write_log(f"Feedback submission failed student_id={student_id}, course_id={course_id}: {traceback.format_exc()}", level="error")
            raise
        finally:
            self.db.disconnect()

    def get_courses(self):
        try:
            self.db.connect()
            cur = self.db.execute("SELECT * FROM courses")
            return cur.fetchall()
        finally:
            self.db.disconnect()
