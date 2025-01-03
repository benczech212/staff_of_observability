from prometheus_client import Counter, Gauge, Summary, Histogram

# Define metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total number of HTTP requests')
REQUEST_LATENCY = Summary('http_request_latency_seconds', 'Request latency in seconds')
ACTIVE_USERS = Gauge('active_users', 'Number of active users')
REQUEST_SIZE = Histogram('http_request_size_bytes', 'Request size in bytes')


TEST_1 = Counter('test_1', 'A simple counter that increments over time')


def increment_request_count():
    REQUEST_COUNT.inc()

def observe_latency(duration):
    REQUEST_LATENCY.observe(duration)

def set_active_users(count):
    ACTIVE_USERS.set(count)

def observe_request_size(size):
    REQUEST_SIZE.observe(size)



def increment_test_1():
    TEST_1.inc()