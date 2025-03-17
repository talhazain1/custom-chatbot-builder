"""
views.py

Defines endpoints for chatbot operations such as running inference on a trained chatbot.
"""

from flask import Blueprint, request, jsonify
from chatbot.models import ChatbotConfig
from chatbot import model_inference

chatbot_bp = Blueprint('chatbot', __name__)
from chatbot.model_inference_openai import run_inference_openai

@chatbot_bp.route('/inference', methods=['POST'])
def chatbot_inference():
    data = request.get_json()
    chatbot_id = data.get('chatbot_id')
    query = data.get('query')
    if not chatbot_id or not query:
        return jsonify({'error': 'chatbot_id and query are required'}), 400

    chatbot_config = ChatbotConfig.query.get(chatbot_id)
    if not chatbot_config:
        return jsonify({'error': 'Chatbot not found'}), 404

    try:
        response_text = run_inference_openai(chatbot_config, query)
        return jsonify({'response': response_text}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
