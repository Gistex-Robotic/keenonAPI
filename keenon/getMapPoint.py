import requests

def get_map_point_v2(base_url, access_token, scene_code, floor_info, case_type, building_info=None):
    """
    Mengambil informasi titik (point) peta V2 berdasarkan scene, lantai, dan tipe bisnis robot.
    :param base_url: URL dasar API
    :param access_token: Token akses Bearer
    :param scene_code: Kode skenario/scene
    :param floor_info: Informasi lantai
    :param case_type: Tipe bisnis robot
    :param building_info: Informasi gedung (opsional)
    :return: Response JSON dari API
    """
    url = base_url.rstrip('/') + '/api/open/custom/robot/v2/map/position'
    headers = {
        'Authorization': f'bearer {access_token}'
    }
    params = {
        'sceneCode': scene_code,
        'floorInfo': floor_info,
        'caseType': case_type
    }
    if building_info:
        params['buildingInfo'] = building_info
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    from keenon_api import API_DOMAIN, get_access_token
    from AxStoreList import get_store_list
    from getSceneList import get_scene_list
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

        # Pilih scene
        scenes_result = get_scene_list(BASE_URL, ACCESS_TOKEN, store_id)
        scenes = []
        if 'data' in scenes_result:
            # Jika data langsung berupa list
            if isinstance(scenes_result['data'], list):
                scenes = scenes_result['data']
            # Jika data dict dengan key 'list'
            elif isinstance(scenes_result['data'], dict) and 'list' in scenes_result['data']:
                scenes = scenes_result['data']['list']
        if not scenes:
            raise RuntimeError("❌ Tidak ada scene ditemukan untuk store ini")
        print("\nDaftar Scene:")
        for idx, scene in enumerate(scenes):
            print(f"{idx + 1}. {scene.get('sceneName', '-')} (Code: {scene.get('sceneCode', '-')})")
        pilih_scene = int(input("Pilih scene nomor berapa? ")) - 1
        scene_code = scenes[pilih_scene]["sceneCode"]

        # Generate daftar floor dari semua robot di store ini
        from AxRobotList import get_robot_list
        from getRobotPosition import get_robot_position
        robot_objs = get_robot_list(ACCESS_TOKEN, store_id)
        floor_set = set()
        for robot in robot_objs:
            sn = robot.get('robotSn') or robot.get('robotId')
            try:
                pos_result = get_robot_position(BASE_URL, ACCESS_TOKEN, store_id, sn)
                if 'data' in pos_result and pos_result['data']:
                    floor = pos_result['data'].get('floor')
                    if floor:
                        floor_set.add(str(floor))
            except Exception:
                continue
        floor_list = sorted(floor_set)
        if not floor_list:
            raise RuntimeError("❌ Tidak ada data floor yang ditemukan dari robot di store ini")
        print("\nDaftar Floor (dari semua robot):")
        for idx, floor in enumerate(floor_list):
            print(f"{idx + 1}. {floor}")
        pilih_floor = int(input("Pilih floor nomor berapa? ")) - 1
        floor_info_raw = floor_list[pilih_floor]
        # Ambil buildingInfo otomatis dari robot pertama
        building_info = None
        if robot_objs:
            sn = robot_objs[0].get('robotSn') or robot_objs[0].get('robotId')
            try:
                pos_result = get_robot_position(BASE_URL, ACCESS_TOKEN, store_id, sn)
                if 'data' in pos_result and pos_result['data']:
                    building_info = pos_result['data'].get('building')
            except Exception:
                pass
        print(f"buildingInfo otomatis: {building_info}")

        # Coba semua caseType umum dan beberapa format floorInfo
        case_types = ["delivery", "cleaning", "charge", "work", "other"]
        floor_info = floor_info_raw  # hanya gunakan "1"
        for case_type in case_types:
            print(f"\nMencoba floorInfo: '{floor_info}', caseType: '{case_type}', buildingInfo: '{building_info}'")
            print(f"Request params: store_id={store_id}, scene_code={scene_code}, floor_info={floor_info}, case_type={case_type}, building_info={building_info}")
            result = get_map_point_v2(BASE_URL, ACCESS_TOKEN, scene_code, floor_info, case_type, building_info)
            print("API Response:", result)
            if 'data' in result and 'targetList' in result['data'] and result['data']['targetList']:
                for point in result['data']['targetList']:
                    print(f"ID: {point.get('id')}, Name: {point.get('name')}, Type: {point.get('type')}, Floor: {point.get('floor')}, X: {point.get('positionX')}, Y: {point.get('positionY')}, Z: {point.get('positionZ')}")
            else:
                print(f"No map point data found for floorInfo: '{floor_info}', caseType: '{case_type}'")
    except Exception as e:
        print(f"Gagal mengambil data map point: {e}")
