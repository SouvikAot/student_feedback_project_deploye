import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="appuser",
        password="AppPassword123!",
        database="feedback_system"
    )
    print("✅ Connection successful.")
    conn.close()
except mysql.connector.Error as err:
    print(f"❌ Connection failed: {err}")
