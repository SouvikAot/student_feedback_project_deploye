import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change_this_to_a_random_secret")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", 3306))
    DB_USER = os.getenv("DB_USER", "appuser")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "AppPassword123!")
    DB_NAME = os.getenv("DB_NAME", "feedback_system")
    LOG_FILE = os.getenv("LOG_FILE", "logs/app.log")
