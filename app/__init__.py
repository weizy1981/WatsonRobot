from flask import Flask

application = Flask(__name__)
application.config.from_object('app.flaskconfig')

from app.view import customerView