from flask import Flask, jsonify, request
from datetime import datetime, timezone
import socket

app = Flask(__name__)


@app.route("/")
def index():
    return jsonify({
        "service": "week7-backend",
        "message": "Hello from the backend application",
        "time_utc": datetime.now(timezone.utc).isoformat(),
        "server_hostname": socket.gethostname(),
        "request_host_header": request.host,
        "request_path": request.path,
        "client_ip": request.remote_addr,
        "x_forwarded_for": request.headers.get("X-Forwarded-For", "not provided")
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "week7-backend",
        "time_utc": datetime.now(timezone.utc).isoformat()
    })


@app.route("/echo/<path:subpath>")
def echo(subpath):
    return jsonify({
        "message": "Echo endpoint reached",
        "subpath": subpath,
        "time_utc": datetime.now(timezone.utc).isoformat(),
        "request_host_header": request.host,
        "client_ip": request.remote_addr
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
