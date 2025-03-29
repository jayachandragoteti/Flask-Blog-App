from flask_sqlalchemy import SQLAlchemy

# Create a SQLAlchemy instance to handle database interactions
# This will be initialized with the Flask app in app/__init__.py
db = SQLAlchemy()
