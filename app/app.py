from flask import Flask, request
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import os
import time

app = Flask(__name__)

# Custom metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['endpoint']
)

@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def record_metrics(response):
    duration = time.time() - request.start_time
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.path,
        status=response.status_code
    ).inc()
    REQUEST_LATENCY.labels(endpoint=request.path).observe(duration)
    return response

@app.route("/")
def home():
    return f"""
    <html>
    <head>
        <style>
            body {{
                background-color: #1a1a2e;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                font-family: Arial, sans-serif;
                color: white;
            }}
            .card {{
                text-align: center;
                background: #16213e;
                padding: 40px 60px;
                border-radius: 16px;
                box-shadow: 0 0 30px rgba(0,200,255,0.2);
            }}
            h1 {{ color: #00d4ff; font-size: 2.5em; }}
            .bike {{ font-size: 5em; }}
            p {{ color: #a0a0c0; font-size: 1.1em; }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="bike">🚴</div>
            <h1>Hello from Kubernetes!</h1>
            <p>Environment: {os.getenv('ENVIRONMENT', 'local')}</p>
            <p>Version: {os.getenv('APP_VERSION', '1.0.0')}</p>
        </div>
    </body>
    </html>
    """

@app.route("/health")
def health():
    return {"status": "healthy"}, 200

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
