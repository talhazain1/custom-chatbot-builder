"""
Main Application Entry Point

Initializes the Flask app, database, blueprints, and monitoring endpoints.
Also serves static files for testing.
"""

import os
from flask import Flask, send_from_directory
from core.database import init_db
from core.monitoring import metrics_endpoint, record_request_data, start_timer, stop_timer
from users.views import users_bp
from admin_panel.views import admin_bp
from chatbot.views import chatbot_bp
from payments.webhook import stripe_webhook

app = Flask(__name__, static_folder="static", static_url_path="")

app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "default_secret_key")

init_db(app)

# Register blueprints
app.register_blueprint(users_bp, url_prefix="/api/users")
app.register_blueprint(admin_bp, url_prefix="/api/admin")
app.register_blueprint(chatbot_bp, url_prefix="/api/chatbot")
app.add_url_rule("/api/payments/webhook", view_func=stripe_webhook, methods=["POST"])
app.add_url_rule("/metrics", view_func=metrics_endpoint, methods=["GET"])
print("SMTP_SERVER:", os.environ.get("SMTP_SERVER"))

@app.before_request
def before_request():
    from flask import request
    request.start_time = start_timer()

@app.after_request
def after_request(response):
    from flask import request
    stop_timer(request.start_time, request.path)
    return record_request_data(request, response)

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5005))
    debug_mode = os.environ.get("DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
