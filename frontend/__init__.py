from flask import Flask


app = Flask(__name__)
app.secret_key = "your_secret_key"

from . import routes