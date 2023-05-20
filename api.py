import requests
import json
from environs import Env
env = Env()
env.read_env()
BASE_URL = env.str('URL')
def create_movie(name=None,description=None,file_id=None):
    response = requests.post(url=f"{BASE_URL}/movie/",data={'name':name,'description':description,"file_id":file_id})
    return response.status_code
def create_user(name=None,telegram_id=None):
    response = requests.post(url=f"{BASE_URL}/user/",
                             data={'name': name, 'telegram_id':telegram_id})
    return response.status_code

def search_movie(key):
    response = requests.get(url=f"{BASE_URL}/movie/?search={key}")
    try:
        data=json.loads(response.text)
        return data
    except:
        data= {"results":[]}
        return data
def get_film(id):
    response = requests.get(url=f"{BASE_URL}/movie/{id}/")
    try:
        data = json.loads(response.text)
        return data
    except:
        return 'Ok'
def get_user(telegram_id):
    response = requests.get(url=f"{BASE_URL}/info/{telegram_id}/")
    data = json.loads(response.text)
    if data=='Not found':
        return 'uz'
    else:
        return data['language']
# Get all users
def get_users():
    response = requests.get(url=f"{BASE_URL}/user/")
    data =  json.loads(response.text)
    return data
def change_language_bot(telegram_id,language):
    response = requests.get(url=f"{BASE_URL}/language/{telegram_id}/{language}/")
    data = json.loads(response.text)
    if data == 'Not found':
        return 'uz'
    else:
        return data['language']