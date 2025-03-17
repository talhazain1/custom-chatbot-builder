"""
User Models

Defines the User model with extended company information and subscription details.
Enforces that one email creates one account (and thus one chatbot).
"""

import datetime
from core.database import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255), nullable=False)
    user_phone = db.Column(db.String(50), nullable=True)
    user_email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    company_id = db.Column(db.Integer, nullable=True)
    company_name = db.Column(db.String(255), nullable=True)
    company_phone = db.Column(db.String(50), nullable=True)
    business_address = db.Column(db.String(512), nullable=True)
    company_website = db.Column(db.String(255), nullable=True)
    company_logo = db.Column(db.String(255), nullable=True)
    niche = db.Column(db.String(255), nullable=True)
    is_verified = db.Column(db.Boolean, default=False)
    # New field: subscription plan (default free_trial)
    subscription_plan = db.Column(db.String(50), default="free_trial")
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.user_email}>"
