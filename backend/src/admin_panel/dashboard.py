"""
Generates aggregated analytics and reports for the admin panel.
Provides insights on total chatbots, interactions, and other key metrics.
"""

from chatbot.models import ChatbotConfig, ChatbotInteraction

def generate_report() -> dict:
    """
    Aggregates key statistics from the database.
    
    Returns:
        dict: Aggregated data including total chatbots, interactions, and a sample breakdown.
    """
    try:
        total_chatbots = ChatbotConfig.query.count()
        total_interactions = ChatbotInteraction.query.count()

        # For more detailed analytics, you can add per-client breakdowns, usage trends, etc.
        report = {
            "total_chatbots": total_chatbots,
            "total_interactions": total_interactions,
            "sample_report": "Further metrics can be added here"
        }
        return report
    except Exception as e:
        raise Exception(f"Error generating dashboard report: {e}")
