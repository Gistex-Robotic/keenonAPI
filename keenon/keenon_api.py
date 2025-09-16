import requests

# Ganti dengan client_id dan client_secret Anda
CLIENT_ID = "1ySP96P697odLMrr"
CLIENT_SECRET = "w19GfvEIAfE9fOL1"
API_DOMAIN = "https://cloud.robotkeenon.com"

def get_access_token():
    url = f"{API_DOMAIN}/api/open/oauth/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    response = requests.post(url, headers=headers, data=data)
    print("Status:", response.status_code)
    print("Response:", response.text)
    response.raise_for_status()
    return response.json()["access_token"]

def get_store_list(access_token):
    url = f"{API_DOMAIN}/api/open/data/v1/store/list"
    headers = {"Authorization": f"bearer {access_token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["data"]

if __name__ == "__main__":
    token = get_access_token()
    stores = get_store_list(token)
    print("Daftar Store:")
    for store in stores:
        print(f"{store['storeId']} - {store['storeName']}")
