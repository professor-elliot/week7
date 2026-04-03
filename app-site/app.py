from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "App is running"

@app.route("/hello")
def hello():
    return jsonify({
        "message": "hello world"
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
