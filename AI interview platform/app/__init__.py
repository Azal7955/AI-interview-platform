from pathlib import Path

from flask import Flask
from flask_login import login_manager

from config import Config
from .extensions import db, login_manager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Create required folders
    Path(app.config["UPLOAD_FOLDER"]).mkdir(
        parents=True,
        exist_ok=True
    )

    Path(app.instance_path).mkdir(
        parents=True,
        exist_ok=True
    )

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Where Flask-Login should redirect unauthenticated users
    login_manager.login_view = "auth.login"

    # Import models
    from .models.user import User
    from .models.resume import Resume
    from .models.interview import Interview

    # IMPORTANT:
    # Tell Flask-Login how to reload a user from the session.
    @login_manager.user_loader
    def load_user(user_id):
        try:
            return User.query.get(int(user_id))
        except (ValueError, TypeError):
            return None

    # Create database tables
    with app.app_context():
        db.create_all()

    # Import routes
    from .routes.main_routes import main_bp
    from .routes.auth_routes import auth_bp
    from .routes.resume_routes import resume_bp
    from .routes.interview_routes import interview_bp

    # Register routes
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(resume_bp)
    app.register_blueprint(interview_bp)

    return app