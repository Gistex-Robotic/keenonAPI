import requests

def get_robot_location(base_url, access_token, robot_sn):
    """
    Mengambil lokasi real-time robot berdasarkan robotSn.
    :param base_url: URL dasar API
    :param access_token: Token akses Bearer
    :param robot_sn: Serial Number robot
    :return: Response JSON dari API
    """
    url = base_url.rstrip('/') + '/api/open/custom/robot/location'
    headers = {
        'Authorization': f'bearer {access_token}'
    }
    params = {
        'robotSn': robot_sn
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    from config import API_DOMAIN
    from AxStoreList import get_access_token, get_store_list
    from AxRobotList import get_robot_list
    BASE_URL = API_DOMAIN
    try:
        ACCESS_TOKEN = get_access_token()
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
            sn = robot.get('robotSn') or robot.get('robotId')
            name = robot.get('robotName', '-')
            print(f"{idx + 1}. {sn} - {name}")
        pilih_robot = int(input("Pilih robot nomor berapa? ")) - 1
        robot_sn = robots[pilih_robot].get('robotSn') or robots[pilih_robot].get('robotId')

        result = get_robot_location(BASE_URL, ACCESS_TOKEN, robot_sn)
        print("\nLokasi Real-Time Robot:")
        if 'data' in result and result['data']:
            data = result['data']
            print(f"Building: {data.get('building')}")
            print(f"Floor: {data.get('floor')}")
            print(f"Coordinate: {data.get('coordinate')}")
            print(f"Take Elevator Status: {data.get('takeElevatorStatus')}")
        else:
            print("No robot location data found.")
    except Exception as e:
        print(f"Gagal mengambil lokasi robot: {e}")
