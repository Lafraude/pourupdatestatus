from flask import Flask, request, jsonify
import time, requests, os

app = Flask(__name__)
active_users = {}

WEBHOOK_URL = "https://discord.com/api/webhooks/1353444682750885908/IFXyAC9N-JTyfei7xHELY42HQi0Gm9JRI40zAf-PudmxwApWMnOu2BLVjCCKDewSnrTF"
MESSAGE_ID_FILE = "message_id.txt"  # Pour stocker l’ID du message créé

def get_active_count():
    now = time.time()
    return sum(1 for t in active_users.values() if now - t < 60)

def build_embed():
    count = get_active_count()

    return {
        "content": "",
        "tts": False,
        "embeds": [
            {
                "color": 2229428,
                "author": {
                    "name": "FIVEPACK",
                    "icon_url": "https://cdn.discordapp.com/attachments/1353365578680766469/1363285117073752245/logo.jpg"
                },
                "fields": [
                    {
                        "name": "Status :",
                        "value": "<:32535applicationapprivedids:1363285894596919417>",
                        "inline": True
                    },
                    {
                        "name": "Downloadable :",
                        "value": "<:2775applicationdeniedids:1363285887277989958>",
                        "inline": True
                    },
                    {
                        "name": "Voici le lien du téléchargement",
                        "value": "[Clique pour télécharger]()",
                        "inline": False
                    },
                    {
                        "name": " ",
                        "value": "----------------------------------------------------"
                    },
                    {
                        "name": "Nombre de spoof total :",
                        "value": "{none}",
                        "inline": False
                    },
                    {
                        "name": "Nombre d'utilisateurs actifs sur l'application :",
                        "value": f"{count}",
                        "inline": False
                    }
                ]
            }
        ],
        "username": "FIVEPACK",
        "avatar_url": "https://cdn.discordapp.com/attachments/1353365578680766469/1363285117073752245/logo.jpg"
    }

def create_or_load_message_id():
    """ Crée le message Discord une fois et récupère son ID. """
    if os.path.exists(MESSAGE_ID_FILE):
        with open(MESSAGE_ID_FILE, "r") as f:
            return f.read().strip()

    # Le message n’existe pas, on le crée via POST
    embed_payload = build_embed()
    response = requests.post(WEBHOOK_URL + "?wait=true", json=embed_payload)

    if response.status_code == 200:
        message_id = response.json()["id"]
        with open(MESSAGE_ID_FILE, "w") as f:
            f.write(message_id)
        return message_id
    else:
        print("❌ Échec de la création du message initial :", response.text)
        return None

def update_webhook():
    message_id = create_or_load_message_id()
    if not message_id:
        return

    embed_payload = build_embed()

    try:
        response = requests.patch(f"{WEBHOOK_URL}/messages/{message_id}", json=embed_payload)
        if response.status_code != 200:
            print("⚠️ PATCH échoué :", response.text)
    except Exception as e:
        print("❌ Erreur lors du PATCH :", e)

@app.route("/ping", methods=["POST"])
def ping():
    data = request.get_json()
    user_id = data.get("id")

    if not user_id:
        return jsonify({"error": "ID manquant"}), 400

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

    # Crée le message embed au démarrage si nécessaire
    create_or_load_message_id()

    app.run(host="0.0.0.0", port=port)
