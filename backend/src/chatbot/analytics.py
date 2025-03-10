"""
Provides functions for logging interactions and retrieving usage analytics for chatbots.
"""

from chatbot.models import ChatbotInteraction
from core.database import db

def log_interaction(chatbot_id: int, user_input: str, bot_response: str):
    """
    Logs a chatbot interaction into the database.
    
    Args:
        chatbot_id (int): ID of the chatbot instance.
        user_input (str): The user's message.
        bot_response (str): The chatbot's response.
    
    Raises:
        Exception: If logging to the database fails.
    """
    try:
        interaction = ChatbotInteraction(
            chatbot_id=chatbot_id,
            user_input=user_input,
            bot_response=bot_response
        )
        db.session.add(interaction)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error logging interaction: {e}")

def get_usage_statistics(chatbot_id: int) -> dict:
    """
    Retrieves usage statistics for a given chatbot, such as the total number of interactions.
    
    Args:
        chatbot_id (int): ID of the chatbot instance.
    
    Returns:
        dict: A dictionary containing usage statistics.
    
    Raises:
        Exception: If the query fails.
    """
    try:
        total_interactions = ChatbotInteraction.query.filter_by(chatbot_id=chatbot_id).count()
        return {"total_interactions": total_interactions}
    except Exception as e:
        raise Exception(f"Error retrieving usage statistics: {e}")
