from flask_login import LoginManager, UserMixin
from dotenv import load_dotenv
from os import getenv
import requests

from frontend import app

load_dotenv()
BASE = getenv('URL_BASE')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User_log(UserMixin):
    def __init__(self, id, email, active):
        self.id = id
        self.email = email
        self.active = active

    @property
    def is_active(self):
        return self.active

@login_manager.user_loader
def load_user(email):
    user = requests.get(f'{BASE}/user/email/{email}')
    if user.status_code == 200:
        data = user.json()
        # перевірку типу отриманих даних
        if isinstance(data, dict):
            return User_log(id=data['id'], email=data['email'], active=True)
        elif isinstance(data, list) and len(data) > 0:
            user_data = data
            return User_log(id=user_data[0], email=user_data[1], active=True)
    return None
