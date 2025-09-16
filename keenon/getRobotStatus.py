import requests

def get_robot_status(base_url, access_token, robot_id):
    """
    Mengambil status robot berdasarkan robotId.
    :param base_url: URL dasar API, contoh: 'https://api.example.com/'
    :param access_token: Token akses Bearer
    :param robot_id: ID unik robot
    :return: Response JSON dari API
    """
    url = base_url.rstrip('/') + '/api/open/scene/v1/robot/status'
    headers = {
        'Authorization': f'bearer {access_token}'
    }
    params = {
        'robotId': robot_id
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    # Ambil BASE_URL dari config.py
    from config import API_DOMAIN
    BASE_URL = API_DOMAIN

    # Ambil ACCESS_TOKEN dari config.py (hasil generate_token)
    from config import ACCESS_TOKEN

    from AxStoreList import get_store_list
    from AxRobotList import get_robot_list

    try:
        # Pilih store
        stores = get_store_list(ACCESS_TOKEN)
        if not stores:
            raise RuntimeError("❌ Tidak ada store ditemukan")
        print("Daftar Store:")
        for idx, store in enumerate(stores):
            print(f"{idx + 1}. {store['storeName']} (ID: {store['storeId']})")
        pilih = int(input("Pilih store nomor berapa? ")) - 1
        store_id = stores[pilih]["storeId"]

        # Pilih robot
        robots = get_robot_list(ACCESS_TOKEN, store_id)
        if not robots:
            raise RuntimeError("❌ Tidak ada robot ditemukan di store ini")
        print("\nDaftar Robot:")
        for idx, robot in enumerate(robots):
            print(f"{idx + 1}. {robot.get('robotName', '-') } (ID: {robot.get('robotId')})")
        pilih_robot = int(input("Pilih robot nomor berapa? ")) - 1
        robot_id = robots[pilih_robot].get('robotId')

        result = get_robot_status(BASE_URL, ACCESS_TOKEN, robot_id)
        print("API Response:", result)
        if 'data' in result and 'list' in result['data']:
            for robot in result['data']['list']:
                print(f"Robot ID: {robot.get('robotId')}, Name: {robot.get('robotName')}, Online: {robot.get('onlineStatus')}, Can Be Called: {robot.get('canBeCalled')}, Charge Status: {robot.get('chargeStatus')}, Power: {robot.get('power')}, Scene: {robot.get('sceneName')}")
        else:
            print("No robot status data found.")
    except Exception as e:
        print(f"Gagal mengambil status robot: {e}")
