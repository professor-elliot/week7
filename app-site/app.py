import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask, jsonify, request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "app.log")

os.makedirs(LOG_DIR, exist_ok=True)

app = Flask(__name__)
app.logger.handlers.clear()
app.logger.setLevel(logging.INFO)

file_handler = RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=2)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(
    logging.Formatter("%(asctime)s %(levelname)s %(message)s")
)

app.logger.addHandler(file_handler)


@app.before_request
def log_request_start():
    app.logger.info(
        "Request received method=%s path=%s remote_addr=%s host=%s",
        request.method,
        request.path,
        request.remote_addr,
        request.host,
    )


@app.route("/")
def index():
    return jsonify(
        {
            "message": "Week 9 backend is running.",
            "tip": "Try /hello, /headers, or /error",
        }
    )


@app.route("/hello")
def hello():
    app.logger.info("Hello endpoint completed successfully")
    return jsonify({"message": "Hello from backend"}), 200


@app.route("/headers")
def headers():
    forwarded_headers = {
        "Host": request.headers.get("Host"),
        "X-Forwarded-For": request.headers.get("X-Forwarded-For"),
        "X-Forwarded-Proto": request.headers.get("X-Forwarded-Proto"),
    }
    app.logger.info("Headers endpoint returned forwarded header data")
    return jsonify(forwarded_headers), 200


@app.route("/error")
def trigger_error():
    app.logger.error("Intentional error endpoint triggered")
    raise RuntimeError("Intentional test error")


@app.errorhandler(Exception)
def handle_exception(exc):
    app.logger.exception("Unhandled exception: %s", exc)
    return jsonify({"error": "Internal Server Error"}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
