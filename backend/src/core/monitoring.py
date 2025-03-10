"""
monitoring.py

Integrates Prometheus metrics for monitoring application performance.
It defines counters and histograms to track request counts and latencies,
and provides helper functions to record these metrics and expose them via a Flask endpoint.
"""

import time
import logging
from flask import Response
from prometheus_client import Counter, Histogram, generate_latest

# Set up basic logging for monitoring events.
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Prometheus metric definitions
REQUEST_COUNT = Counter(
    'flask_request_count',
    'Application Request Count',
    ['method', 'endpoint', 'http_status']
)
REQUEST_LATENCY = Histogram(
    'flask_request_latency_seconds',
    'Request latency in seconds',
    ['endpoint']
)

def record_request_data(request, response):
    """
    Record metrics for an incoming request and its response.
    
    Args:
        request: The Flask request object.
        response: The Flask response object.
    
    Returns:
        The original response.
    """
    try:
        REQUEST_COUNT.labels(
            request.method, request.path, response.status_code
        ).inc()
    except Exception as e:
        logger.error(f"Error recording request count: {e}")
    return response

def start_timer():
    """
    Start a timer to measure request duration.
    
    Returns:
        float: The current time in seconds.
    """
    return time.time()

def stop_timer(start_time, endpoint):
    """
    Stop the timer and record the elapsed time in a histogram metric.
    
    Args:
        start_time (float): The time when the request started.
        endpoint (str): The endpoint path for the request.
    
    Returns:
        float: The elapsed time in seconds.
    """
    elapsed = time.time() - start_time
    try:
        REQUEST_LATENCY.labels(endpoint).observe(elapsed)
    except Exception as e:
        logger.error(f"Error recording request latency: {e}")
    return elapsed

def metrics_endpoint():
    """
    Flask endpoint to expose Prometheus metrics.
    
    Returns:
        Response: A Flask response containing all Prometheus metrics in plain text.
    """
    return Response(generate_latest(), mimetype='text/plain')
