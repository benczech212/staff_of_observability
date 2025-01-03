from flask import Flask, request
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from app.metrics import increment_request_count, observe_latency, observe_request_size, increment_test_1

import time

app = Flask(__name__)

@app.route('/metrics')
def metrics():
    """Expose Prometheus metrics."""
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.route('/process')
def process_request():
    """Simulate processing a request."""
    start_time = time.time()

    # Simulate some work
    request_size = len(request.args)  # Simulate request size
    observe_request_size(request_size)
    time.sleep(1)

    increment_request_count()
    duration = time.time() - start_time
    observe_latency(duration)

    return f"Request processed in {duration:.2f} seconds", 200

@app.route('/increment_test_1')
def increment_test_1_endpoint():
    """Increment the test_1 metric."""
    increment_test_1()
    return "test_1 incremented!", 200
