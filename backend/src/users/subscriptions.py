"""
User Subscriptions Module

Handles updating and managing user subscriptions.
Ensures that each user gets the features tied to their chosen package.
"""

from core.database import db
from users.models import User

def subscribe_user(user_id: int, subscription_plan: str) -> bool:
    try:
        user = User.query.get(user_id)
        if not user:
            raise Exception("User not found")
        user.subscription_plan = subscription_plan
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Subscription update failed: {e}")
