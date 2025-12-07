import requests


BASE_URL = "https://jsonplaceholder.typicode.com/users"


def get_all_users():
    response = requests.get(BASE_URL)
    response.raise_for_status()
    return response.json()

def get_user(id):
    response = requests.get(f"{BASE_URL}/{id}")
    response.raise_for_status()
    return response.json()


def create_user(data):
    response = requests.post(BASE_URL,json=data)
    response.raise_for_status()
    return response.json()

def update_user(id,data):
    response = requests.put(f"{BASE_URL}/{id}",json=data)
    response.raise_for_status()
    return response().json()

def delete_user(id):
    response = requests.delete(f"{BASE_URL}/{id}")
    response.raise_for_status()
    return {"message":"User deleted successfully"}