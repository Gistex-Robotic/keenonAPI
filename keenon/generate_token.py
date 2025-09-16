import time
import requests
from config import CLIENT_ID, CLIENT_SECRET, API_DOMAIN

CONFIG_PATH = 'config.py'

def get_access_token():
    url = f"{API_DOMAIN}/api/open/oauth/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()["access_token"]

def update_config_access_token(token):

    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    found = False
    for i, line in enumerate(lines):
        if line.strip().startswith('ACCESS_TOKEN'):
            lines[i] = f'ACCESS_TOKEN = "{token}"\n'
            found = True
            break
    if not found:
        lines.append(f'ACCESS_TOKEN = "{token}"\n')
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        f.writelines(lines)

def main():
    while True:
        try:
            token = get_access_token()
            update_config_access_token(token)
            print(f"ACCESS_TOKEN updated: {token}")
        except Exception as e:
            print("Gagal mendapatkan access_token:", e)
        time.sleep(3600)  # 1 jam

if __name__ == "__main__":
    main()
