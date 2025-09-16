
import requests
from keenon_api import API_DOMAIN, get_store_list
from config import CLIENT_ID, CLIENT_SECRET
from generate_token import get_access_token
from getSceneList import get_scene_list
from AxRobotList import get_robot_list
from getRobotPosition import get_robot_position

def get_robot_map(access_token, scene_code, floor_info, building_info=None, save_to_file=None):
    """
    Mengambil data peta robot dari API dan menyimpan hasilnya ke file jika diinginkan.
    
    :param base_url: URL dasar API, contoh: 'https://api.example.com/'
    :param access_token: Token akses Bearer
    :param scene_code: Kode scene (wajib)
    :param floor_info: Informasi lantai (wajib)
    :param building_info: Informasi gedung (opsional)
    :param save_to_file: Nama file untuk menyimpan hasil binary (opsional)
    :return: Response JSON dan path file jika disimpan
    """
    url = API_DOMAIN.rstrip('/') + '/api/open/custom/robot/map'
    headers = {
        'Authorization': f'bearer {access_token}'
    }
    params = {
        'sceneCode': scene_code,
        'floorInfo': floor_info
    }
    if building_info:
        params['buildingInfo'] = building_info

    response = requests.get(url, headers=headers, params=params, stream=True)
    response.raise_for_status()
    data = response.json()
    content = data.get('data', {}).get('content', None)

    file_path = None
    if content and save_to_file:
        # Jika content berupa base64, decode dulu. Jika byte[], simpan langsung.
        import base64
        try:
            decoded = base64.b64decode(content)
            with open(save_to_file, 'wb') as f:
                f.write(decoded)
            file_path = save_to_file
        except Exception:
            pass
    return data, file_path

if __name__ == "__main__":
    # Generate token setiap run
    token = get_access_token()

    # Default values sesuai permintaan user
    store_id = "C00712322"  # GM3_1
    scene_code = "iSs8Yu"   # GM3_GM1
    scene_name = "GM3_GM1"
    robot_sn = "2C:C3:E6:E7:F2:0E"  # ZURI
    floor_info = "1"
    building_info = None
    default_filename = f"{scene_code}_{scene_name}.png".replace(' ', '_')
    save_to = default_filename

    result, file_path = get_robot_map(token, scene_code, floor_info, building_info, save_to)
    print("API Response:", result)
    if file_path:
        # Cek signature PNG
        with open(file_path, 'rb') as f:
            sig = f.read(8)
        if sig == b'\x89PNG\r\n\x1a\n':
            print(f"Map data saved to {file_path} (PNG detected)")
        else:
            print(f"Map data saved to {file_path}, tetapi file ini bukan PNG valid!")
    else:
        print("No map data saved.")
