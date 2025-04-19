from flask import Flask, request, jsonify
import time, requests, os

app = Flask(__name__)
active_users = {}

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")

def get_active_count():
    now = time.time()
    return sum(1 for t in active_users.values() if now - t < 60)

def update_webhook():
    count = get_active_count()

    embed_payload = {
        "content": "",
        "tts": False,
        "embeds": [
            {
                "id": 815429150,
                "color": 2229428,
                "author": {
                    "name": "FIVEPACK",
                    "icon_url": "https://cdn.discordapp.com/attachments/1353365578680766469/1363285117073752245/logo.jpg?ex=680579b4&is=68042834&hm=f2cf62ba061ca4ea129f08ea4687a57e9c5526b950816a399ecf9b04c7a3696e&"
                },
                "fields": [
                    {
                        "id": 780596281,
                        "name": "Status :",
                        "value": ":32535applicationapprivedids:",
                        "inline": True
                    },
                    {
                        "id": 240109194,
                        "name": "Downloadable :",
                        "value": ":2775applicationdeniedids:",
                        "inline": True
                    },
                    {
                        "id": 197967438,
                        "name": "Voici le lien du téléchargement",
                        "value": "[Clique pour télécharger]()",
                        "inline": False
                    },
                    {
                        "id": 309815222,
                        "name": " ",
                        "value": " ----------------------------------------------------"
                    },
                    {
                        "id": 75380828,
                        "name": "Nombre de spoof total :",
                        "value": "{none}",
                        "inline": False
                    },
                    {
                        "id": 6574565,
                        "name": "Nombre d'utilisateurs actifs sur l'application :",
                        "value": f"{count}",
                        "inline": False
                    }
                ]
            }
        ],
        "components": [],
        "actions": {},
        "username": "FIVEPACK",
        "avatar_url": "https://cdn.discordapp.com/attachments/1353365578680766469/1363285117073752245/logo.jpg?ex=680579b4&is=68042834&hm=f2cf62ba061ca4ea129f08ea4687a57e9c5526b950816a399ecf9b04c7a3696e&"
    }

    try:
        requests.patch(WEBHOOK_URL, json=embed_payload)
    except Exception as e:
        print("Erreur lors de la mise à jour du webhook :", e)

@app.route("/ping", methods=["POST"])
def ping():
    data = request.get_json()
    user_id = data.get("id")
    active_users[user_id] = time.time()
    update_webhook()
    return jsonify({"status": "pong"})

@app.route("/stats", methods=["GET"])
def stats():
    return jsonify({"active_users": get_active_count()})

@app.route("/")
def home():
    return "API opérationnelle ✅"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
