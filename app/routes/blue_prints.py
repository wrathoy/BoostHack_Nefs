from flask import Blueprint

# Import all route blueprints
from app.routes.auth import auth_bp
from app.routes.user import user_bp
from app.routes.reservaion import reservation_bp

# Create a Blueprint for all routes (optional, if needed)
routes_bp = Blueprint('routes', __name__)

# List of blueprints to register in the app
blueprints = [
    (user_bp, "/"),
    (auth_bp, "/auth"),
    (reservation_bp, "/reservation"),

]

def register_routes(app):
    """Registers all blueprints with their respective prefixes."""
    for blueprint, prefix in blueprints:
        app.register_blueprint(blueprint, url_prefix=prefix)