"""
utils.py

Provides utility functions for the application, including JWT token generation and verification.
Secrets are loaded from environment variables to ensure security.
"""

import os
import jwt
import datetime

# Get the secret key from environment variables (ensure you set this in your production environment)
SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')

def generate_jwt(payload, exp_minutes=60):
    """
    Generate a JWT token with an expiration time.
    
    Args:
        payload (dict): Data to encode in the token.
        exp_minutes (int): Token expiration time in minutes.
    
    Returns:
        str: Encoded JWT token.
    """
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=exp_minutes)
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    # Ensure the token is a string (for compatibility across jwt versions)
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token

def verify_jwt(token):
    """
    Verify a JWT token and return its payload if valid.
    
    Args:
        token (str): The JWT token to verify.
    
    Returns:
        dict or None: Decoded payload if token is valid; otherwise, None.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        # Token has expired
        return None
    except jwt.InvalidTokenError:
        # Token is invalid
        return None
