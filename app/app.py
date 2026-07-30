from flask import Flask
import os

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
