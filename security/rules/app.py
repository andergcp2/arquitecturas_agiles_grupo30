from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/rules")
def root():
    return jsonify({'ruleId': 36}), 200

@app.route("/check")
def check():
    return jsonify({"status": "up"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0')