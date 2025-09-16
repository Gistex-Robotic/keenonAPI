import requests

def get_point_list(base_url, access_token, scene_code):
    """
    Mengambil daftar point berdasarkan scene ID.
    :param base_url: URL dasar API, contoh: 'https://api.example.com/'
    :param access_token: Token akses Bearer
    :param scene_code: ID scene
    :return: Response JSON dari API
    """
    url = base_url.rstrip('/') + '/api/open/scene/v1/target/list'
    headers = {
        'Authorization': f'bearer {access_token}'
    }
    params = {
        'sceneCode': scene_code
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    # Ambil BASE_URL dari config.py
    from config import API_DOMAIN
    BASE_URL = API_DOMAIN

    # Ambil fungsi get_access_token dari AxStoreList.py
    from AxStoreList import get_access_token

    try:
        ACCESS_TOKEN = get_access_token()
        scene_code = input("Masukkan sceneCode (ID scene): ")
        result = get_point_list(BASE_URL, ACCESS_TOKEN, scene_code)
        print("API Response:", result)
        if 'data' in result and 'list' in result['data']:
            for point in result['data']['list']:
                print(f"Point Name: {point.get('pointName')}, Area: {point.get('area')}, UUID: {point.get('uuid')}, Point ID: {point.get('pointId')}")
        else:
            print("No point data found.")
    except Exception as e:
        print(f"Gagal mengambil daftar point: {e}")
