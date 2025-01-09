from flask import Flask
from flask_socketio import SocketIO
from event_handlers import initialize_all_handlers

from dotenv import load_dotenv
from os import getenv 

import json

with open('./config.json') as f:
    config = json.load(f)

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = getenv('SECRET_KEY')

socketio = SocketIO(app, cors_allowed_origins=config['CORS_origin'])

initialize_all_handlers(socketio)

if __name__ == "__main__":
    socketio.run(app, port=config['port'], host='0.0.0.0' if config['LAN'] else '127.0.0.1')
