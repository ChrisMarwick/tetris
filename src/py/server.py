from flask import Flask, request
from game_event import GameEvent
from game import Game
from uuid import uuid4
from flask_socketio import SocketIO, emit


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')


games = {}

def get_game(request):
    global games
    room_id = request.sid
    try:
        game = games[room_id]
    except KeyError:
        raise Exception('Error: Game not found')
    return game


def generate_client_gateway(room_id: str):
    def client_message_gateway(event: GameEvent, data: dict):
        socketio.emit('event', {
            'event': event.value,
            'data': data
        }, to=room_id)

    return client_message_gateway


@socketio.on('new_game')
def handle_new_game():
    room_id = request.sid
    print('Creating a new game with room_id:', room_id)
    global games
    games.pop(room_id, None)

    callback = generate_client_gateway(room_id)
    games[room_id] = Game(callback)
    games[room_id].start()
    # Should we be using room_id/sid as the game id?
    emit('new_game', {'game_id': room_id})


@socketio.on('action')
def handle_action(message):
    game = get_game(request)

    # Process actions from the client
    for event in GameEvent:
        if message['event'] == event.value:
            game.dispatch_event(event)
            break


if __name__ == '__main__':
    socketio.run(app)
