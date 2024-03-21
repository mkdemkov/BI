import requests


async def get_workspace():
    response = requests.get("http://127.0.0.1:8000/get_workspace")
    return response.json()


async def load_data():
    response = requests.get("http://127.0.0.1:8000/export_workspace")
    return response.json()


async def import_data(data):
    data_json_compatible = [list(item) for item in data]
    response = requests.post(url="http://127.0.0.1:8000/import_data", json=data_json_compatible)
    return response.json()
