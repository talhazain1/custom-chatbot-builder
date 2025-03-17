"""
Admin Panel Views

Exposes endpoints for managing and customizing chatbot configurations.
Each endpoint is scoped to the logged-in user's company so that a company admin sees only its own data.
"""

import json
from flask import Blueprint, request, jsonify
from admin_panel import services, dashboard
from core.utils import verify_jwt
from users.models import User

admin_bp = Blueprint('admin', __name__)

def get_logged_in_company_id():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return None, jsonify({"error": "Authorization header missing"}), 401
    token = auth_header.split(" ")[-1]
    payload = verify_jwt(token)
    if not payload:
        return None, jsonify({"error": "Invalid or expired token"}), 401
    user_id = payload.get("user_id")
    user = User.query.get(user_id)
    if not user:
        return None, jsonify({"error": "User not found"}), 404
    # Use company_id if available, otherwise fallback to user's id.
    return user.company_id or user.id, None, None

@admin_bp.route('/chatbots', methods=['GET'])
def list_chatbots():
    company_id, error_response, status = get_logged_in_company_id()
    if error_response:
        return error_response, status
    try:
        # Filter chatbots by the logged-in company's id.
        chatbots = services.get_all_chatbots(company_id)
        chatbots_data = [services.chatbot_to_dict(bot) for bot in chatbots]
        return jsonify(chatbots_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/chatbots/<int:chatbot_id>', methods=['GET'])
def get_chatbot(chatbot_id):
    company_id, error_response, status = get_logged_in_company_id()
    if error_response:
        return error_response, status
    try:
        chatbot = services.get_chatbot_by_id(chatbot_id)
        if not chatbot or chatbot.company_id != company_id:
            return jsonify({"error": "Chatbot not found for your company"}), 404
        return jsonify(services.chatbot_to_dict(chatbot)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/chatbots', methods=['POST'])
def create_chatbot():
    company_id, error_response, status = get_logged_in_company_id()
    if error_response:
        return error_response, status
    try:
        if request.content_type.startswith("multipart/form-data"):
            # Retrieve standard form fields from request.form
            company_id_form = request.form.get("company_id")
            # In a secure implementation, we ignore any passed company_id and use the one from the token.
            configuration = request.form.get("configuration", "{}")
            purpose = request.form.get("purpose")
            goal = request.form.get("goal")
            role = request.form.get("role")
            payment_plan = request.form.get("payment_plan", "free_trial")
            
            # Handle text input and file for knowledge base.
            knowledge_base_text = request.form.get("knowledge_base")
            kb_file = request.files.get("knowledge_base_file")
            knowledge_base = {}
            
            if kb_file:
                file_content = kb_file.read().decode("utf-8")
                try:
                    knowledge_base = json.loads(file_content)
                except Exception as e:
                    knowledge_base = {"faqs": [{"question": "", "answer": file_content.strip()}]}
            elif knowledge_base_text:
                try:
                    knowledge_base = json.loads(knowledge_base_text)
                except Exception:
                    knowledge_base = {"faqs": [{"question": "", "answer": knowledge_base_text.strip()}]}
            if isinstance(configuration, str):
                configuration = json.loads(configuration)
            
            payload = {
                "company_id": company_id,  # Always use the logged in user's company id
                "configuration": configuration,
                "purpose": purpose,
                "goal": goal,
                "role": role,
                "payment_plan": payment_plan,
                "knowledge_base": knowledge_base
            }
        else:
            payload = request.get_json()
            payload["company_id"] = company_id  # Use the logged-in company id.
        
        # Create chatbot using our services.
        chatbot = services.create_chatbot(payload)
        return jsonify(services.chatbot_to_dict(chatbot)), 201
    except Exception as e:
        return jsonify({"error": "Error creating chatbot", "details": str(e)}), 500

@admin_bp.route('/chatbots/<int:chatbot_id>', methods=['PUT'])
def update_chatbot(chatbot_id):
    company_id, error_response, status = get_logged_in_company_id()
    if error_response:
        return error_response, status
    try:
        data = request.get_json()
        chatbot = services.get_chatbot_by_id(chatbot_id)
        if not chatbot or chatbot.company_id != company_id:
            return jsonify({"error": "Chatbot not found for your company"}), 404
        chatbot = services.update_chatbot_config(chatbot_id, data)
        return jsonify(services.chatbot_to_dict(chatbot)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/chatbots/<int:chatbot_id>', methods=['DELETE'])
def delete_chatbot(chatbot_id):
    company_id, error_response, status = get_logged_in_company_id()
    if error_response:
        return error_response, status
    try:
        chatbot = services.get_chatbot_by_id(chatbot_id)
        if not chatbot or chatbot.company_id != company_id:
            return jsonify({"error": "Chatbot not found for your company"}), 404
        result = services.delete_chatbot(chatbot_id)
        return jsonify({"message": "Chatbot deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/chatbots/<int:chatbot_id>/retrain', methods=['POST'])
def retrain_chatbot(chatbot_id):
    company_id, error_response, status = get_logged_in_company_id()
    if error_response:
        return error_response, status
    try:
        data = request.get_json()
        knowledge_base = data.get("knowledge_base")
        new_config = data.get("configuration", {})
        chatbot = services.get_chatbot_by_id(chatbot_id)
        if not chatbot or chatbot.company_id != company_id:
            return jsonify({"error": "Chatbot not found for your company"}), 404
        chatbot = services.retrain_chatbot(chatbot_id, knowledge_base, new_config)
        return jsonify(services.chatbot_to_dict(chatbot)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/dashboard', methods=['GET'])
def get_dashboard():
    company_id, error_response, status = get_logged_in_company_id()
    if error_response:
        return error_response, status
    try:
        data = dashboard.generate_dashboard(company_id)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
