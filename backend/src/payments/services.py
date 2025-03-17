"""
services.py

This module provides higher-level payment services. It wraps the Stripe integration functions,
adding business logic as needed. For example, it initiates a checkout session and returns the URL
for the client to complete payment.
"""

from payments import stripe_integration

def initiate_payment(customer_email: str, price_id: str, success_url: str, cancel_url: str) -> str:
    """
    Initiate the payment process by creating a Stripe Checkout session.
    The subscription is configured to auto-renew every month.
    
    Args:
        customer_email (str): The customer's email address.
        price_id (str): The Stripe price ID for the subscription.
        success_url (str): The URL to which the customer is redirected after a successful payment.
        cancel_url (str): The URL to which the customer is redirected if the payment is canceled.
    
    Returns:
        str: The URL of the created checkout session.
    
    Raises:
        Exception: If the checkout session creation fails.
    """
    try:
        # Additional subscription metadata can be passed if needed.
        session = stripe_integration.create_checkout_session(
            customer_email=customer_email,
            price_id=price_id,
            success_url=success_url,
            cancel_url=cancel_url
        )
        return session.url
    except Exception as e:
        # In production, log the error and handle it appropriately.
        raise Exception(f"Failed to initiate payment: {e}")
