from flask import Flask, request, jsonify
import time

app = Flask(__name__)
active_users = {}

@app.route("/ping", methods=["POST"])
def ping():
    user_id = request.json.get("id")
    active_users[user_id] = time.time()
    return jsonify({"status": "ok"})

@app.route("/stats", methods=["GET"])
def stats():
    now = time.time()
    active = [uid for uid, ts in active_users.items() if now - ts < 60]
    return jsonify({"active_users": len(active)})

@app.route("/", methods=["GET"])
def home():
    return "Serveur actif ✅"
