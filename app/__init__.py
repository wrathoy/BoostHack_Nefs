from flask import Flask
from app.database import create_tables
from app.routes.blue_prints import register_routes  # Import function from __init__.py
from flask_session import Session


def create_app():
    """Initialize and configure the Flask application."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    # Configure session to use filesystem (instead of signed cookies)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"

    # Initialize the session
    Session(app)

    # Ensure database tables exist
    create_tables()

    # Register all routes from routes/__init__.py
    register_routes(app)

    return app