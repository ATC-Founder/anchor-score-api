from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from AnchorScore!"

@app.route("/health")
def health_check():
    return jsonify({"status": "ok", "message": "AnchorScore API is running"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
