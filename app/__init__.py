from flask import Flask
from app.controller.watsonLanguage import WatsonConversation

application = Flask(__name__)
application.config.from_object('app.flaskconfig')

conversation = WatsonConversation()

from app.view import customerView