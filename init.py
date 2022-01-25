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
monster = 1

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


def rotatePlayers():
    if getCurrentActivePlayer() is None:
        players[0].is_current = True
        players[1].is_next = True
    else:
        getCurrentActivePlayer().is_current = False
        next_player = getNextActivePlayer()
        next_player.is_current = True
        next_player.is_next = False

        # Get index of new next player
        index = players.index(next_player)
        new_next_player_index = 0
        if index != len(players) - 1:
            new_next_player_index = index + 1

        players[new_next_player_index].is_next = True


def findPlayer(name):
    for player in players:
        if player.name == name:
            return player
    print("couldn't find player")
    return


def updatePlayers(request):
    for player in players:
        if player.name in request:
            player.initiative = int(request[player.name])
            print(player.name + " updated to " + request[player.name])


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
        players.append(Character(i['name'], 10, True, i['dexterity'], i['ac'], i['pass_int'], i['pass_per'], True))
    print(players)
    # Closing file
    f.close()


@app.route("/", methods=['GET', 'POST'])
def index():
    # First time only
    resetCharacters()
    return redirect(url_for('dashboard'))


@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        if 'button' in request.form:
            if request.form['button'] == 'add_player':
                return redirect(url_for('add_character'))
            elif request.form['button'] == 'sort':
                updatePlayers(request.form)
                players.sort(key=attrgetter('initiative'), reverse=True)
            elif request.form['button'] == 'next':
                rotatePlayers()
                print("Current: " + getCurrentActivePlayer().name)
                print("Next: " + getNextActivePlayer().name)
            elif request.form['button'] == 'reset':
                resetCharacters()
            else:
                pass  # unknown
        if 'enable' in request.form:
            Character.toggle_enabled(findPlayer(request.form['enable']))
        elif 'remove' in request.form:
            #remove temp player
            index = players.index(findPlayer(request.form['remove']))
            del players[index]
        elif 'monster' in request.form:
            #add generic monster
            global monster
            players.append(Character(
            "Monster " + str(monster),
            0,
            True,
            10,
            0,0,0,False))
            monster = monster + 1
        return render_template("dyn.html", content=players)
    elif request.method == 'GET':
        return render_template("dyn.html", content=players)


@app.route("/add_character", methods=['GET', 'POST'])
def add_character():
    if request.method == 'POST':
        selected = request.form.getlist('enabled-input')
        any_selected = bool(selected)

        players.append(Character(
            request.form['name-input'],
            int(request.form['initiative-input']),
            any_selected,
            int(request.form['dexterity-input']),
            0,0,0,False

            #TODO: need way to enter additional char data - if required
            #TODO: Checkbox on screen to determine if prompt for additonal data
        ))
        return redirect(url_for('dashboard'))
    elif request.method == 'GET':
        return render_template("add_characters.html")


if __name__ == "__main__":
    app.run(debug=True)
