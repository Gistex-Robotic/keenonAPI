import requests
from config import CLIENT_ID, CLIENT_SECRET, API_DOMAIN

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

def get_robot_list(access_token, store_id):
    url = f"{API_DOMAIN}/api/open/data/v1/store/robot/list"
    headers = {"Authorization": f"bearer {access_token}"}
    params = {"storeId": store_id}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()["data"]

if __name__ == "__main__":
    try:
        token = get_access_token()
        store_id = input("Masukkan Store ID: ")
        robots = get_robot_list(token, store_id)
        print("Daftar Robot:")
        for robot in robots:
            print(f"{robot['robotId']} - {robot['robotName']} - Online: {robot['onlineStatus']} - Power: {robot['power']} - Model: {robot.get('robotModel', '-')} - App: {robot.get('appVersion', '-')} - City: {robot.get('city', '-')} - OnlineType: {robot.get('onlineType', '-')} ")
    except Exception as e:
        print("Terjadi error:", e)
