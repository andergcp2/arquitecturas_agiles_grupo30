from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/rules")
def root():
    return jsonify({'ruleId': 3}, {'ruleId': 6}, {'ruleId': 9}), 200

@app.route("/check")
def check():
    return jsonify({"status": "rules command running"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0')