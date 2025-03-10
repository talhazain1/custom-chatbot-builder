"""
Defines the SQLAlchemy models for chatbot configurations and interactions.
"""

from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
from core.database import db

class ChatbotConfig(db.Model):
    __tablename__ = 'chatbot_configs'
    
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, nullable=False)
    configuration = db.Column(JSON, nullable=False)  # Stores all configuration settings
    purpose = db.Column(db.String(255), nullable=True)  # e.g. "customer support", "sales"
    goal = db.Column(db.String(255), nullable=True)     # e.g. "resolve queries", "generate leads"
    role = db.Column(db.String(255), nullable=True)     # e.g. "assistant", "advisor"
    knowledge_base = db.Column(JSON, nullable=True)
    trained_model = db.Column(db.LargeBinary, nullable=True)  # Storing pickled model
    last_trained_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<ChatbotConfig id={self.id} client_id={self.client_id}>"

class ChatbotInteraction(db.Model):
    __tablename__ = 'chatbot_interactions'
    
    id = db.Column(db.Integer, primary_key=True)
    chatbot_id = db.Column(db.Integer, db.ForeignKey('chatbot_configs.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_input = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<ChatbotInteraction chatbot_id={self.chatbot_id} timestamp={self.timestamp}>"
