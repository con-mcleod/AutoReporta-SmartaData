import os
from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = os.urandom(12)

login_manager = LoginManager()
login_manager.init_app(app)