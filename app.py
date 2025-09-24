from flask import Flask
import os
from config import Config

# Ensure logs directory exists
os.makedirs(os.path.dirname(Config.LOG_FILE), exist_ok=True)


# Blueprints
from routes.student_routes import student_bp
from routes.admin_routes import admin_bp

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(Config)

    os.makedirs(os.path.dirname(app.config['LOG_FILE']), exist_ok=True)

    # Register blueprints
    app.register_blueprint(student_bp)
    app.register_blueprint(admin_bp)

    # Simple index route
    @app.route('/')
    def index():
        return "Student Feedback Management System - Visit /register or /login"

    return app

def list_routes(app):
    import urllib
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(sorted(rule.methods))
        line = urllib.parse.unquote(f"{rule.endpoint:30s} {methods:20s} {rule}")
        output.append(line)
    for line in sorted(output):
        print(line)

# Add this at the bottom of app.py
app = create_app()

if __name__ == "__main__":
    print("\n=== Registered Routes ===")
    list_routes(app)
    print("=========================\n")
    app.run(debug=True, host="0.0.0.0", port=5000)


# #if __name__ == "__main__":
#     app = create_app()
#     app.run(debug=True, host="0.0.0.0", port=5000)
