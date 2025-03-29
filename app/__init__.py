from flask import Flask
from dotenv import load_dotenv
from app.models import db
from flask_migrate import Migrate
import os

# Load environment variables
load_dotenv()

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
    
    # Configure the database URI
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///default.db")
    
    # Initialize database and migrations
    db.init_app(app)
    Migrate(app, db)
    
    return app
