from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def home():
    return "App is running"

@app.route("/hello", methods=["GET"])
def hello():
    return jsonify({
        "message": "hello world"
    })

@app.route("/hello", methods=["POST"])
def hello_post():
    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({
            "error": "name is required"
        }), 400

    name = data["name"]

    return jsonify({
        "message": f"hello {name}"
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
