"""
Admin panel API endpoints for managing and customizing chatbots.
Clients can view, update, create, delete, and re‐train their chatbot configurations.
"""

import json
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from admin_panel import services, dashboard

admin_bp = Blueprint('admin', __name__)

# Endpoint: Get all chatbots (optionally filtered by client_id)
@admin_bp.route('/chatbots', methods=['GET'])
def list_chatbots():
    client_id = request.args.get('client_id', type=int)
    try:
        chatbots = services.get_all_chatbots(client_id)
        # Convert SQLAlchemy objects to dictionaries
        chatbots_data = [services.chatbot_to_dict(bot) for bot in chatbots]
        return jsonify(chatbots_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint: Get a specific chatbot configuration by ID
@admin_bp.route('/chatbots/<int:chatbot_id>', methods=['GET'])
def get_chatbot(chatbot_id):
    try:
        chatbot = services.get_chatbot_by_id(chatbot_id)
        if not chatbot:
            return jsonify({"error": "Chatbot not found"}), 404
        return jsonify(services.chatbot_to_dict(chatbot)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint: Create a new chatbot configuration
@admin_bp.route('/chatbots', methods=['POST'])
def create_chatbot():
    try:
        # Expecting JSON body with client_id, configuration and dynamic fields (purpose, goal, role)
        data = request.get_json()
        chatbot = services.create_chatbot(data)
        return jsonify(services.chatbot_to_dict(chatbot)), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint: Update an existing chatbot configuration
@admin_bp.route('/chatbots/<int:chatbot_id>', methods=['PUT'])
def update_chatbot(chatbot_id):
    try:
        data = request.get_json()
        chatbot = services.update_chatbot_config(chatbot_id, data)
        if not chatbot:
            return jsonify({"error": "Chatbot not found"}), 404
        return jsonify(services.chatbot_to_dict(chatbot)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint: Delete a chatbot configuration
@admin_bp.route('/chatbots/<int:chatbot_id>', methods=['DELETE'])
def delete_chatbot(chatbot_id):
    try:
        result = services.delete_chatbot(chatbot_id)
        if not result:
            return jsonify({"error": "Chatbot not found"}), 404
        return jsonify({"message": "Chatbot deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint: Retrain a chatbot with updated knowledge base and/or configuration.
# Supports file upload for a new knowledge base JSON.
@admin_bp.route('/chatbots/<int:chatbot_id>/retrain', methods=['POST'])
def retrain_chatbot():
    chatbot_id = request.view_args['chatbot_id']
    try:
        # Check if a file was uploaded; alternatively, JSON knowledge base can be provided.
        if 'knowledge_base' in request.files:
            file = request.files['knowledge_base']
            filename = secure_filename(file.filename)
            # For demonstration, load the file content directly; in production, you may want to save it temporarily.
            knowledge_base = json.load(file)
        else:
            # Alternatively, the knowledge base can be sent as JSON in the body
            knowledge_base = request.get_json().get('knowledge_base')
        
        # New configuration data (optional) for dynamic fields update
        new_config = request.get_json().get('configuration', {})

        chatbot = services.retrain_chatbot(chatbot_id, knowledge_base, new_config)
        if not chatbot:
            return jsonify({"error": "Chatbot not found or retraining failed"}), 404
        return jsonify(services.chatbot_to_dict(chatbot)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint: Dashboard for aggregated analytics and usage data
@admin_bp.route('/dashboard', methods=['GET'])
def dashboard_data():
    try:
        data = dashboard.generate_report()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
