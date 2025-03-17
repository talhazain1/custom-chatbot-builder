"""
Stripe Integration Module

Creates Stripe Checkout sessions for subscriptions with auto-renewal.
Collects card info for free trials without immediate charge.
"""

import os
import stripe

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "sk_test_default")

def create_checkout_session(customer_email: str, price_id: str, success_url: str, cancel_url: str, subscription_data: dict = None):
    if subscription_data is None:
        subscription_data = {}
    subscription_data.setdefault("metadata", {})["auto_renew"] = "true"

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='subscription',
            line_items=[{"price": price_id, "quantity": 1}],
            subscription_data=subscription_data,
            customer_email=customer_email,
            success_url=success_url + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=cancel_url,
        )
        return session
    except stripe.error.StripeError as e:
        raise e
