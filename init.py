from operator import attrgetter
from socket import socket

from flask import Flask, render_template, request, redirect, url_for, flash
from characters import Character
from ws4py.client.threadedclient import WebSocketClient

app = Flask(__name__)
app.secret_key = "hello"

character_names = ["Shanko", "Saelwyn",
                   "Kaelar", "Owly", "Tree", "Gith", "Otadus"]
players = []
monster = 1
sequence_started = False

esp8266host = "ws://192.168.1.65:81/"


class DummyClient(WebSocketClient):
    def opened(self):
        print("Websocket open")

    def closed(self, code, reason=None):
        print("Connection closed down", code, reason)

    def received_message(self, m):
        print(m)


def getCurrentActivePlayer():
    if len(players) < 2:
        return
    for char in players:
        if char.is_current:
            return char
    # Didn't find one
    return None


def getNextActivePlayer():
    for char in players:
        if char.is_next:
            return char
    return


def findNextEnabledPlayer(start_index):
    if start_index >= len(players):
        start_index = 0
    for i in range(start_index, len(players) - 1):
        if players[i].enabled and not players[i].is_current and not players[i].is_next:
            return players[i]

    for i in range(0, start_index):
        if players[i].enabled and not players[i].is_current and not players[i].is_next:
            return players[i]


def rotatePlayers():
    enabled_player_count = 0
    for player in players:
        if player.enabled:
            enabled_player_count = enabled_player_count + 1

    if enabled_player_count < 3:
        flash("Not enough enabled players!")
        return

    if getCurrentActivePlayer() is None:
        findNextEnabledPlayer(0).is_current = True
        findNextEnabledPlayer(0).is_next = True

    else:
        # Current player is no longer current, moved to what was previously next player
        getCurrentActivePlayer().is_current = False
        next_player = getNextActivePlayer()
        next_player.is_current = True
        next_player.is_next = False

        # New next player found here
        findNextEnabledPlayer(players.index(next_player)).is_next = True


def findPlayer(name):
    for player in players:
        if player.name == name:
            return player
    print("couldn't find player")
    return


def updatePlayers(update_request):
    if sequence_started:
        flash("Cannot sort once sequence has started!")
        return

    for player in players:
        if player.name in update_request:
            if not update_request[player.name]:
                flash("Must set all initiatives first!")
                return
            player.initiative = int(update_request[player.name])
            print(player.name + " updated to " + update_request[player.name])


def resetCharacters():
    global monster
    monster = 1
    players.clear()

    import json

    # Opening JSON file
    f = open('data.json')

    # returns JSON object as
    # a dictionary
    data = json.load(f)

    # Iterating through the json
    # list
    for i in data['players']:
        print(i)
        players.append(Character(
            str(i['name']),
            int(10),
            True,
            int(i['dexterity']),
            int(i['ac']),
            int(i['pass_int']),
            int(i['pass_per']),
            True))
    print(players)
    # Closing file
    f.close()


def sortPlayers():
    players.sort(key=lambda player: (-player.initiative, -player.dexterity, player.name))


@app.route("/", methods=['GET', 'POST'])
def index():
    # First time only
    resetCharacters()
    return redirect(url_for('dashboard'))


@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    global sequence_started
    if request.method == 'POST':
        if 'button' in request.form:
            if request.form['button'] == 'add_player':
                return redirect(url_for('add_character'))
            elif request.form['button'] == 'sort':
                updatePlayers(request.form)
                sortPlayers()
            elif request.form['button'] == 'next':
                sequence_started = True
                rotatePlayers()
            elif request.form['button'] == 'reset':
                sequence_started = False
                resetCharacters()
            else:
                pass  # unknown
        if 'enable' in request.form:
            Character.toggle_enabled(findPlayer(request.form['enable']))
        elif 'remove' in request.form:
            updatePlayers(request.form)
            # remove temp player
            index = players.index(findPlayer(request.form['remove']))
            del players[index]
        elif 'monster' in request.form:
            updatePlayers(request.form)
            # add generic monster
            global monster
            players.append(Character(
                "Monster " + str(monster),
                0,
                True,
                10,
                0, 0, 0, False))
            monster = monster + 1
        return render_template("dyn.html", content=players)
    elif request.method == 'GET':
        return render_template("dyn.html", content=players)


@app.route("/add_character", methods=['GET', 'POST'])
def add_character():
    if request.method == 'POST':
        if 'back' in request.form:
            return redirect(url_for('dashboard'))

        selected = request.form.getlist('enabled-input')
        any_selected = bool(selected)

        players.append(Character(
            request.form['name-input'],
            int(request.form['initiative-input']),
            any_selected,
            int(request.form['dexterity-input']),
            0, 0, 0, False
        ))

        sortPlayers()

        return redirect(url_for('dashboard'))
    elif request.method == 'GET':
        return render_template("add_characters.html")


if __name__ == "__main__":
    app.run(debug=True)
