import requests
from config import CLIENT_ID, CLIENT_SECRET, API_DOMAIN, ACCESS_TOKEN
from datetime import datetime

class AxRecord:
	def __init__(self, store_id, access_token=None):
		self.store_id = store_id
		self.access_token = access_token or ACCESS_TOKEN

	def get_food_task_records(self, page=1, size=20, start_time=None, end_time=None):
		url = f"{API_DOMAIN}/api/open/data/v1/store/task/food/list"
		headers = {"Authorization": f"bearer {self.access_token}"}
		params = {
			"storeId": self.store_id,
			"page": page,
			"size": size
		}
		if start_time:
			params["startTime"] = start_time
		if end_time:
			params["endTime"] = end_time
		response = requests.get(url, headers=headers, params=params)
		response.raise_for_status()
		return response.json()["data"]

def date_to_millis(date_str):
	# Format: YYYY-MM-DD
	dt = datetime.strptime(date_str, "%Y-%m-%d")
	return int(dt.timestamp() * 1000)

if __name__ == "__main__":
	store_id = input("Masukkan Store ID: ")
	start_date = input("Tanggal mulai (YYYY-MM-DD, kosongkan jika tidak ingin filter): ")
	end_date = input("Tanggal akhir (YYYY-MM-DD, kosongkan jika tidak ingin filter): ")
	ax_record = AxRecord(store_id)
	try:
		start_time = date_to_millis(start_date) if start_date else None
		end_time = date_to_millis(end_date) if end_date else None
		data = ax_record.get_food_task_records(start_time=start_time, end_time=end_time)
		print(f"Total record: {data.get('total', 0)}")
		for record in data.get('list', []):
			print(f"Robot: {record.get('robotId', '-')}, Start: {record.get('startTime', '-')}, End: {record.get('endTime', '-')}, Status: {record.get('taskStatus', '-')}, Mileage: {record.get('taskMileage', '-')}m")
	except Exception as e:
		print("Terjadi error:", e)
