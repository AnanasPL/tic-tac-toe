from flask_socketio import SocketIOTestClient

def set_up_the_room(client_maker, number: int = 1) -> tuple[str, SocketIOTestClient]:
    # Creating room
    client = client_maker()
    client.emit('create-room')
    code = client.get_received()[1]['args'][0]
    
    
    clients = []
    
    for _ in range(number):
        client = client_maker()
        client.emit('join-room', code)
        clients.append(client)

    return code, *(client for client in clients)