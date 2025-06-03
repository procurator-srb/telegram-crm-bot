import json
import time
import requests

SECRETS_FILE = "secrets.json"

def load_secrets():
    with open(SECRETS_FILE, "r") as f:
        return json.load(f)

def save_secrets(data):
    with open(SECRETS_FILE, "w") as f:
        json.dump(data, f)

def get_access_token():
    secrets = load_secrets()
    now = int(time.time())

    if secrets.get("access_token") and now < secrets.get("expires_at", 0):
        return secrets["access_token"]

    response = requests.post("https://accounts.zoho.eu/oauth/v2/token", data={
        "refresh_token": secrets["refresh_token"],
        "client_id": secrets["client_id"],
        "client_secret": secrets["client_secret"],
        "grant_type": "refresh_token"
    })

    token_data = response.json()
    secrets["access_token"] = token_data["access_token"]
    secrets["expires_at"] = now + int(token_data.get("expires_in", 3600)) - 60

    save_secrets(secrets)
    return secrets["access_token"]
