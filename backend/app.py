from flask import Flask
from flask_socketio import SocketIO
from event_handlers import initialize_all_handlers

from dotenv import load_dotenv
from os import getenv 

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = getenv('SECRET_KEY')

socketio = SocketIO(app, cors_allowed_origins='*')

initialize_all_handlers(socketio)


if __name__ == "__main__":
    socketio.run(app, port=5000)
