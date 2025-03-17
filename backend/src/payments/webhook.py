"""
webhook.py

This module handles incoming Stripe webhook events. It verifies the Stripe signature
and processes events such as checkout session completions, recurring invoice payments,
and subscription deletions.
"""

import os
import json
import stripe
from flask import request, jsonify

# Load the webhook secret from the environment.
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "whsec_default")

def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature", None)
    if not sig_header:
        return jsonify({"error": "Missing Stripe-Signature header"}), 400

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        # Invalid payload
        return jsonify({"error": "Invalid payload"}), 400
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return jsonify({"error": "Invalid signature"}), 400

    event_type = event.get("type")
    data_object = event.get("data", {}).get("object", {})

    # Process events
    if event_type == "checkout.session.completed":
        handle_checkout_session_completed(data_object)
    elif event_type == "invoice.payment_succeeded":
        handle_invoice_payment_succeeded(data_object)
    elif event_type == "customer.subscription.deleted":
        handle_subscription_deleted(data_object)
    # Additional events can be handled as needed.

    return jsonify({"status": "success"}), 200

def handle_checkout_session_completed(session: dict):
    """
    Process a completed checkout session.
    
    Args:
        session (dict): The checkout session object from Stripe.
    """
    # Typically, create or update your subscription record in your database here.
    print("Checkout session completed:", session)

def handle_invoice_payment_succeeded(invoice: dict):
    """
    Process a successful recurring invoice payment.
    This event confirms that an auto-renewal charge has been processed.
    
    Args:
        invoice (dict): The invoice object from Stripe.
    """
    # Extract subscription info from the invoice metadata if needed.
    subscription_id = invoice.get("subscription")
    amount_paid = invoice.get("amount_paid")
    currency = invoice.get("currency")
    print(f"Auto-renewal payment succeeded for subscription {subscription_id}: {amount_paid} {currency}")
    # TODO: Update your database records for the subscription renewal, log the transaction, etc.

def handle_subscription_deleted(subscription: dict):
    """
    Process a subscription deletion event.
    
    Args:
        subscription (dict): The subscription object from Stripe.
    """
    print("Subscription deleted:", subscription)
    # TODO: Update your database to mark the subscription as canceled.
