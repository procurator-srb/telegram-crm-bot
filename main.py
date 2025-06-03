import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

ACCESS_TOKEN = "1000.a4c362733420519e35a98cb73d2e7311.bebdb3f7b0ede6511006a929a1c89130"
API_DOMAIN = "https://www.zohoapis.eu"
HEADERS = {
    "Authorization": f"Zoho-oauthtoken {ACCESS_TOKEN}"
}

def create_lead(from_user, message_text):
    url = f"{API_DOMAIN}/crm/v2/Leads"
    data = {
        "data": [{
            "Last_Name": f"Telegram {from_user}",
            "Company": "Telegram Inquiry",
            "Description": message_text
        }]
    }
    response = requests.post(url, json=data, headers=HEADERS)
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
