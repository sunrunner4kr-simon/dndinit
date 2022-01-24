from operator import attrgetter
from socket import socket

from flask import Flask, render_template, request, redirect, url_for
from characters import Character
from ws4py.client.threadedclient import WebSocketClient

app = Flask(__name__)
app.secret_key = "hello"

character_names = ["Shanko", "Saelwyn",
                   "Kaelar", "Owly", "Tree", "Gith", "Otadus"]
players = []

esp8266host = "ws://192.168.1.65:81/"


class DummyClient(WebSocketClient):
    def opened(self):
        print("Websocket open")

    def closed(self, code, reason=None):
        print("Connection closed down", code, reason)

    def received_message(self, m):
        print(m)


def findPlayer(name):
    for player in players:
        if player.name == name:
            return player
    print("couldn't find player")
    return


def updatePlayers(request):
    for player in players:
        if player.name in request:
            player.initiative = request[player.name]
            print(player.name + " updated to " + request[player.name])


@app.route("/", methods=['GET', 'POST'])
def index():
    # First time only
    players.clear()
    for char in character_names:
        players.append(Character(char, 10, True))

    return redirect(url_for('dashboard'))


@ app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        if 'button' in request.form:
            if request.form['button'] == 'add_player':
                return redirect(url_for('add_character'))
            elif request.form['button'] == 'sort':
                updatePlayers(request.form)
                players.sort(key=attrgetter('initiative'), reverse=True)
            elif request.form['button'] == 'reset':
                players.clear()
                for char in character_names:
                    players.append(Character(char, 10, True))
            else:
                pass  # unknown
        if 'enable' in request.form:
            Character.toggle_enabled(findPlayer(request.form['enable']))
        return render_template("dyn.html", content=players)
    elif request.method == 'GET':
        return render_template("dyn.html", content=players)


@ app.route("/add_character", methods=['GET', 'POST'])
def add_character():
    if request.method == 'POST':
        selected = request.form.getlist('enabled-input')
        any_selected = bool(selected)

        players.append(Character(
            request.form['name-input'],
            int(request.form['initiative-input']),
            any_selected
        ))
        return redirect(url_for('dashboard'))
    elif request.method == 'GET':
        return render_template("add_characters.html")


if __name__ == "__main__":
    app.run(debug=True)
