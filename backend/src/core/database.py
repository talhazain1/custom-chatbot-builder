"""
database.py

This module initializes the PostgreSQL database connection using Flask-SQLAlchemy.
It reads configuration from environment variables and sets up connection pooling options.
"""

import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """
    Initialize the database with the Flask application.
    
    The configuration is read from environment variables:
      - DATABASE_URL: PostgreSQL connection URL.
      - POOL_SIZE, MAX_OVERFLOW, POOL_TIMEOUT, POOL_RECYCLE: Connection pooling options.
    
    This setup is intended for production use.
    """
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 'postgresql://user:password@localhost:5432/chatbotdb'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "pool_size": int(os.environ.get("POOL_SIZE", 10)),
        "max_overflow": int(os.environ.get("MAX_OVERFLOW", 20)),
        "pool_timeout": int(os.environ.get("POOL_TIMEOUT", 30)),
        "pool_recycle": int(os.environ.get("POOL_RECYCLE", 1800)),
    }
    
    db.init_app(app)
    with app.app_context():
        db.create_all()
