import os
from flask import Flask
from dotenv import load_dotenv

# Load environment variables
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))

# Import extensions
from app.extensions import db, migrate

def create_app():
    """
    Factory function to create and configure a Flask app instance.
    """
    app = Flask(
        __name__, 
        template_folder="templates",
        static_folder="static",
        static_url_path='/'
    )
    
    # Configure app settings
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(BASE_DIR, 'db/blog_app_db.db')}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default_secret_key")
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    from app.routes import main, auth, blog 
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(blog)

    return app
