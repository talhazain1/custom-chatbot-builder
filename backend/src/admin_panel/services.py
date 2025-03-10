"""
Business logic for managing chatbot configurations.
Handles CRUD operations, re-training, and conversion to dictionary format.
"""

import json
from chatbot.models import ChatbotConfig
from core.database import db
from chatbot import builder, model_training, data_processing

def chatbot_to_dict(chatbot: ChatbotConfig) -> dict:
    """Converts a ChatbotConfig SQLAlchemy object to a dictionary."""
    return {
        "id": chatbot.id,
        "client_id": chatbot.client_id,
        "configuration": chatbot.configuration,
        "purpose": chatbot.purpose,
        "goal": chatbot.goal,
        "role": chatbot.role,
        "knowledge_base": chatbot.knowledge_base,
        "last_trained_at": chatbot.last_trained_at.isoformat() if chatbot.last_trained_at else None,
    }

def get_all_chatbots(client_id: int = None):
    """Retrieve all chatbots; optionally filter by client_id."""
    if client_id:
        return ChatbotConfig.query.filter_by(client_id=client_id).all()
    return ChatbotConfig.query.all()

def get_chatbot_by_id(chatbot_id: int):
    """Retrieve a specific chatbot by ID."""
    return ChatbotConfig.query.get(chatbot_id)

def create_chatbot(data: dict) -> ChatbotConfig:
    """
    Create a new chatbot configuration.
    Expected keys in data: client_id, configuration, purpose, goal, role, and optionally knowledge_base.
    If a knowledge base is provided, it will be preprocessed and used to train the model.
    """
    try:
        client_id = data.get("client_id")
        configuration = data.get("configuration", {})
        purpose = data.get("purpose")
        goal = data.get("goal")
        role = data.get("role")
        knowledge_base = data.get("knowledge_base", {})

        # Preprocess the knowledge base if provided and train the model.
        processed_kb = data_processing.preprocess_knowledge_base(knowledge_base) if knowledge_base else {}
        trained_model = model_training.train_model(processed_kb, configuration) if processed_kb else None

        chatbot = ChatbotConfig(
            client_id=client_id,
            configuration=configuration,
            purpose=purpose,
            goal=goal,
            role=role,
            knowledge_base=processed_kb,
            trained_model=trained_model
        )
        db.session.add(chatbot)
        db.session.commit()
        return chatbot
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error creating chatbot: {e}")

def update_chatbot_config(chatbot_id: int, data: dict) -> ChatbotConfig:
    """
    Update an existing chatbot configuration.
    Allows updating dynamic fields as well as the static configuration.
    """
    chatbot = get_chatbot_by_id(chatbot_id)
    if not chatbot:
        return None

    try:
        chatbot.configuration = data.get("configuration", chatbot.configuration)
        chatbot.purpose = data.get("purpose", chatbot.purpose)
        chatbot.goal = data.get("goal", chatbot.goal)
        chatbot.role = data.get("role", chatbot.role)

        # Optionally update knowledge base and re-train if new knowledge base is provided.
        new_kb = data.get("knowledge_base")
        if new_kb:
            processed_kb = data_processing.preprocess_knowledge_base(new_kb)
            chatbot.knowledge_base = processed_kb
            chatbot.trained_model = model_training.train_model(processed_kb, chatbot.configuration)
        
        db.session.commit()
        return chatbot
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error updating chatbot: {e}")

def delete_chatbot(chatbot_id: int) -> bool:
    """Delete a chatbot configuration."""
    chatbot = get_chatbot_by_id(chatbot_id)
    if not chatbot:
        return False
    try:
        db.session.delete(chatbot)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error deleting chatbot: {e}")

def retrain_chatbot(chatbot_id: int, new_knowledge_base: dict, new_config: dict = None) -> ChatbotConfig:
    """
    Re-train the chatbot with a new knowledge base and/or new configuration.
    The new configuration (if provided) will override existing settings.
    """
    chatbot = get_chatbot_by_id(chatbot_id)
    if not chatbot:
        return None
    try:
        # Update configuration if new settings are provided
        if new_config:
            chatbot.configuration.update(new_config)
            chatbot.purpose = new_config.get("purpose", chatbot.purpose)
            chatbot.goal = new_config.get("goal", chatbot.goal)
            chatbot.role = new_config.get("role", chatbot.role)
        
        # Preprocess and train model with new knowledge base
        processed_kb = data_processing.preprocess_knowledge_base(new_knowledge_base)
        chatbot.knowledge_base = processed_kb
        chatbot.trained_model = model_training.train_model(processed_kb, chatbot.configuration)
        
        db.session.commit()
        return chatbot
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error retraining chatbot: {e}")
