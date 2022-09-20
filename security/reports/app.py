from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/reports")
def root():
    return jsonify({'reportId': 72}), 200

@app.route("/check")
def check():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0')