import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

API_DOMAIN = "https://www.zohoapis.eu"

def get_access_token():
    url = "https://accounts.zoho.eu/oauth/v2/token"
    data = {
        "refresh_token": os.environ.get("ZOHO_REFRESH_TOKEN"),
        "client_id": os.environ.get("ZOHO_CLIENT_ID"),
        "client_secret": os.environ.get("ZOHO_CLIENT_SECRET"),
        "grant_type": "refresh_token"
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()["access_token"]

def create_lead(telegram_id, username, message_text):
    access_token = get_zoho_access_token()
    url = "https://www.zohoapis.eu/crm/v2/Leads"
    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}"
    }

    data = {
        "data": [
            {
                "Last_Name": f"Telegram {telegram_id}",
                "Company": "Telegram Inquiry",
                "Lead_Source": "Telegram",
                "Telegram_ID": int(telegram_id),
                "Telegram_username": username,
                "Telegram_message": message_text,
                "Telegram_status": "Новый"
            }
        ]
    }

    response = requests.post(url, json=data, headers=headers)
    print("ZOHO RESPONSE:", response.status_code, response.text)

@app.route("/", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    if "message" in data:
        msg = data["message"]
        user = msg.get("from", {}).get("username", "Unknown")
        text = msg.get("text", "")
        create_lead(user, text)
    return jsonify({"status": "received"})

@app.route("/", methods=["GET"])
def index():
    return "Бот работает!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
