import requests

def get_scene_list(base_url, access_token, store_id):
    """
    Mengambil daftar scene berdasarkan store ID.
    :param base_url: URL dasar API, contoh: 'https://api.example.com/'
    :param access_token: Token akses Bearer
    :param store_id: ID toko/store
    :return: Response JSON dari API
    """
    url = base_url.rstrip('/') + '/api/open/scene/v1/info/list'
    headers = {
        'Authorization': f'bearer {access_token}'
    }
    params = {
        'storeId': store_id
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    # Ambil BASE_URL dari config.py
    from config import API_DOMAIN
    BASE_URL = API_DOMAIN

    # Ambil fungsi get_access_token dan get_store_list dari AxStoreList.py
    from AxStoreList import get_access_token, get_store_list

    try:
        ACCESS_TOKEN = get_access_token()
        stores = get_store_list(ACCESS_TOKEN)
        if not stores:
            print("Tidak ada store yang ditemukan.")
            exit(1)
        print("Pilih Store:")
        for idx, store in enumerate(stores):
            print(f"{idx+1}. {store['storeId']} - {store['storeName']}")
        pilihan = input("Masukkan nomor store yang dipilih: ")
        try:
            pilihan_idx = int(pilihan) - 1
            if pilihan_idx < 0 or pilihan_idx >= len(stores):
                raise ValueError
        except Exception:
            print("Pilihan tidak valid.")
            exit(1)
        STORE_ID = stores[pilihan_idx]['storeId']
    except Exception as e:
        print(f"Gagal mengambil daftar store: {e}")
        exit(1)

    result = get_scene_list(BASE_URL, ACCESS_TOKEN, STORE_ID)
    print("API Response:", result)
    if 'data' in result and 'list' in result['data']:
        for scene in result['data']['list']:
            print(f"Scene Code: {scene.get('sceneCode')}, Scene Name: {scene.get('sceneName')}")
    else:
        print("No scene data found.")
