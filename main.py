from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def root():
    return jsonify({"status": "OK", "message": "Welcome to AnchorScore API"})

@app.route("/healthz")
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
