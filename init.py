import time

from operator import attrgetter
from socket import socket
from rpi_ws281x import Color, PixelStrip, ws

from flask import Flask, render_template, request, redirect, url_for, flash
from characters import Character
from seats import Seat

# LED strip configuration:
LED_COUNT = 91         # Number of LED pixels.
LED_PIN = 18           # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000   # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10           # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 100   # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_INVERT = False
LED_CHANNEL = 0
LED_STRIP = ws.SK6812_STRIP_RGBW

app = Flask(__name__)
app.secret_key = "hello"

character_names = ["Shanko", "Saelwyn",
                   "Kaelar", "Owly", "Tree", "Gith", "Otadus"]
players = []
playerSeats = []
monster = 1
npc = 1
sequence_started = False

add = ""

def setupSeats():
      playerSeats.clear()
      import json

      # Opening JSON file
      f = open('seats.json')

      # returns JSON object as
      # a dictionary
      data = json.load(f)
      
      # Iterating through the json
      # list
      for i in data['seats']:
          playerSeats.append(Seat(
                int(i['seat']),
                int(i['start']),
                int(i['length'])))
      # Closing file
      f.close()


def setCurrentSeat(start, numPixels):
    for i in range(start, numPixels):
        strip.setPixelColor(i, Color(0, 255, 0))
        strip.setBrightness(255)
        strip.show()


def setNextSeat(start, numPixels):
    for i in range(start, numPixels):
        strip.setPixelColor(i, Color(255, 0, 0))
        strip.setBrightness(255)
        strip.show()


def findSeat(playerName):
    for x in ( player for player in players if player.name == playerName):
        for i in playerSeats:
            if i.seat == x.seat:
                return i
    
    return None


def setSeatInactive(player):
    inactiveSeat = findSeat(player.name)
    if inactiveSeat is not None:
        for i in range(inactiveSeat.start, inactiveSeat.length, 1):
            strip.setPixelColor(i, Color(255, 255, 255))
            strip.setBrightness(100)
            strip.show()


def setAllSeats():
    for i in range(0, 14, 1):
            strip.setPixelColor(i, Color(0, 255, 0))
            strip.setBrightness(100)
            strip.show()
    for i in range(14, 91, 1):
            strip.setPixelColor(i, Color(255, 255, 255))
            strip.setBrightness(100)
            strip.show()

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
    for i in range(start_index, len(players)):
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
        currentPlayer = findNextEnabledPlayer(0)
        currentPlayer.is_current = True
        nextPlayer = findNextEnabledPlayer(0)
        nextPlayer.is_next = True
        # Get seat details for player seat
        newseat = findSeat(currentPlayer.name)
        if newseat is not None:
            setCurrentSeat(newseat.start, newseat.length)
        if newseat is not findSeat(nextPlayer.name):
            newseat = findSeat(nextPlayer.name)
            if newseat is not None: 
                setNextSeat(newseat.start, newseat.length)
    else:
        # Current player is no longer current, moved to what was previously next player
        currentPlayer = getCurrentActivePlayer()
        currentPlayer.is_current = False
        print("Setting last current false: " + currentPlayer.name)
        # set white
        setSeatInactive(currentPlayer)
        next_player = getNextActivePlayer()
        next_player.is_current = True
        print("Setting new current true: " + next_player.name)
        next_player.is_next = False
        print("Setting new current next false: " + next_player.name)
        nextSeat = findSeat(next_player.name)
        setCurrentSeat(nextSeat.start, nextSeat.length)
        print("Set Current Seat: " + next_player.name)

        # New next player found here
        nextPlayer = findNextEnabledPlayer(players.index(next_player))
        nextPlayer.is_next = True
        print("Setting new next true: " + nextPlayer.name)
        if findSeat(next_player.name) is not findSeat(nextPlayer.name):
            setNextSeat(findSeat(nextPlayer.name).start, findSeat(nextPlayer.name).length)
            print("Set Next Seat: " + nextPlayer.name)


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
        if "DEX" + player.name in update_request:
            player.dexterity = int(update_request["DEX"+player.name])
            print(player.name + " dex updated to " +
                  update_request["DEX"+player.name])


def resetCharacters():
    global monster
    monster = 1
    global npc
    npc = 1
    global add
    add = ""
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
        players.append(Character(
            str(i['name']),
            int(10),
            True,
            int(i['dexterity']),
            int(i['ac']),
            int(i['pass_int']),
            int(i['pass_per']),
            True, False, int(i['seat'])))
    print("Players created")
    # Closing file
    f.close()
    setupSeats()
    setAllSeats()

def sortPlayers():
    players.sort(key=lambda player: (-player.initiative, -
                 player.dexterity, player.name))


def checkDex(dex_request):
    list = players
    for player in players:
        if "DEX" + player.name in dex_request and player.dexterity == 0:

            for item in list:
                if item.initiative == player.initiative and item.name is not player.name:

                    return player.name
    return None


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
                if checkDex(request.form) is None:
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
                10,
                True,
                0,
                0, 0, 0, False, True, 1))
            monster = monster + 1
        elif 'npc' in request.form:
            updatePlayers(request.form)
            # add generic monster
            global npc
            players.append(Character(
                "NPC " + str(npc),
                10,
                True,
                0,
                0, 0, 0, False, False, 1))
            npc = npc + 1
        count = len([elem for elem in players if elem.is_player == False])
        global add
        if count == 8:
            add = "disabled"
        return render_template("dyn.html", content=players, add=add, dex=checkDex(request.form))
    elif request.method == 'GET':
        return render_template("dyn.html", content=players, add=add)


@app.route("/add_character", methods=['GET', 'POST'])
def add_character():
    if request.method == 'POST':
        if 'back' in request.form:
            return redirect(url_for('dashboard'))
        print(request.form)

        players.append(Character(
            request.form['name-input'],
            int(request.form['initiative-input']),
            True,
            int(request.form['dexterity-input']),
            0, 0, 0, False, False, int(request.form['seat-input'])
        ))

        sortPlayers()

        return redirect(url_for('dashboard'))
    elif request.method == 'GET':
        return render_template("add_characters.html")


if __name__ == "__main__":
    # Create NeoPixel object with appropriate configuration.
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA,
                       LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    app.run(debug=True)
