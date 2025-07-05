from flask import Flask, request
from flask_socketio import SocketIO, emit

from game_event import GameEvent
from game import Game


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


games = {}


def get_game(request):
    """
    After a game is created we store it in memory, keyed against an id. This way other handlers that happen after the
    creation can access the game object.
    """
    room_id = request.sid
    try:
        game = games[room_id]
    except KeyError as ex:
        raise RuntimeError("Error: Game not found") from ex
    return game


def generate_client_gateway(room_id: str):
    """
    The room id is dynamic so we need to bind a new callback function everytime a game is created.
    """
    def client_message_gateway(event: GameEvent, data: dict):
        socketio.emit("event", {"event": event.value, "data": data}, to=room_id)

    return client_message_gateway


@app.route("/")
def index():
    """Simple healthcheck to check the server is running and correcting routing requests."""
    return "Hello"


@socketio.on("new_game")
def handle_new_game():
    """
    Create a new game object and map an id to it, this is how different handlers are able to route to the active game
    post creation.
    """
    room_id = request.sid
    print("Creating a new game with room_id:", room_id)
    games.pop(room_id, None)

    callback = generate_client_gateway(room_id)
    games[room_id] = Game(callback)
    games[room_id].start()
    # Should we be using room_id/sid as the game id?
    emit("new_game", {"game_id": room_id})


@socketio.on("action")
def handle_action(message):
    """
    Shuttle actions emitted from the frontend to the event handler.
    """
    game = get_game(request)

    # Process actions from the client
    for event in GameEvent:
        if message["event"] == event.value:
            game.dispatch_event(event)
            break


if __name__ == "__main__":
    socketio.run(app)
