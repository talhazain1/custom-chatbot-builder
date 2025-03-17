"""
Chatbot Models

Defines the models for chatbot configuration, interactions, chat logs, and training data.
"""

from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
from core.database import db

class ChatbotConfig(db.Model):
    __tablename__ = 'chatbot_configs'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, nullable=False)
    # External chatbot identifier if needed.
    chatbot_id = db.Column(db.String(64), nullable=True)
    role = db.Column(db.String(255), nullable=True)
    payment_plan = db.Column(db.String(50), nullable=True)
    version = db.Column(db.Integer, default=1)
    configuration = db.Column(JSON, nullable=True)
    purpose = db.Column(db.String(255), nullable=True)
    goal = db.Column(db.String(255), nullable=True)
    knowledge_base = db.Column(JSON, nullable=True)
    trained_model = db.Column(db.LargeBinary, nullable=True)
    last_trained_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ChatbotConfig id={self.id} company_id={self.company_id}>"

class ChatbotInteraction(db.Model):
    __tablename__ = 'chatbot_interactions'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, nullable=False)
    chatbot_id = db.Column(db.Integer, nullable=False)
    chat_id = db.Column(db.String(64), nullable=False)
    messages = db.Column(JSON, nullable=True)  # List of messages (conversation log)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ChatbotInteraction chat_id={self.chat_id}>"

class Chat(db.Model):
    __tablename__ = 'chats'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, nullable=False)
    chatbot_id = db.Column(db.Integer, nullable=False)
    chat_id = db.Column(db.String(64), nullable=False)
    messages = db.Column(JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Chat chat_id={self.chat_id}>"

class Train(db.Model):
    __tablename__ = 'train_data'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, nullable=False)
    chatbot_id = db.Column(db.Integer, nullable=False)
    faqs = db.Column(JSON, nullable=True)    # FAQs used for training.
    queries = db.Column(JSON, nullable=True) # Past queries for analysis.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<TrainData chatbot_id={self.chatbot_id}>"
