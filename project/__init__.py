import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    """
    This function creates a Flask application instance with the necessary configurations.

    Returns:
    Flask: A Flask application instance.
    """
    main = Flask(__name__)

    # Generate a secret key
    secret_key = os.urandom(24).hex()
    # Set the secret key for the Flask application
    main.config['SECRET_KEY'] = secret_key
    main.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'

    db.init_app(main)

    login_manager = LoginManager()
    # Set the login view for the login manager
    login_manager.login_view = 'auth.login'
    login_manager.init_app(main)

    from .models import User

    with main.app_context():
        # Create tables defined in models
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        """
        This function loads a user by their ID.

        Args:
        user_id (int): The ID of the user to load.

        Returns:
        User: The loaded user object.
        """
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    # Register the authentication blueprint
    main.register_blueprint(auth_blueprint)

    from project.main import main as main_blueprint
    # Register the main blueprint
    main.register_blueprint(main_blueprint)

    return main
