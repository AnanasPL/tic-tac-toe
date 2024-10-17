from flask import Flask
from flask_socketio import SocketIO
from event_handlers import initialize_all_handlers

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')

initialize_all_handlers()

if __name__ == "__main__":
    socketio.run(app, port=5000, debug=True)
    