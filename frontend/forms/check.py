from flask import (
    redirect,
    url_for
)

from dotenv import load_dotenv
from os import getenv

load_dotenv('.env.example')
BASE = getenv('URL_BASE')

import requests

def check_role(email:str):
    print(email)
    user_response = requests.get(url=f'{BASE}/user/email/{email}')

    if user_response.status_code == 200:
        user = user_response.json()
        print(user)
        if type(user) == list:
            return 'error'
        else:
            if user['role_id'] == 2:
                return 'candidate'
            else:
                return 'employer'
    else:
        return None