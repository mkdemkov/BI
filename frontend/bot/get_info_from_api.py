import requests


async def get_workspace():
    response = requests.get("http://127.0.0.1:8000/get_workspace")
    return response.json()
