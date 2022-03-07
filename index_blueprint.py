from flask import render_template, request, redirect, url_for, flash, Blueprint
from characters import Character
from seats import Seat


index_blueprint = Blueprint('index', __name__)

playerSeats = []
monster = 1
npc = 1
sequence_started = False

add = ""


# def setupSeats():
#    playerSeats.clear()
#    import json

# Opening JSON file
#    f = open('seats.json')

# returns JSON object as
# a dictionary
#    data = json.load(f)

# Iterating through the json
# list
#    for i in data['seats']:
#        playerSeats.append(Seat(
#            int(i['seat']),
#            int(i['start']),
#            int(i['length'])))
# Closing file
#    f.close()


# def setCurrentSeat(start, numPixels):
#    for i in range(start, numPixels):
#        strip.setPixelColor(i, Color(255, 0, 0))
#        strip.setBrightness(255)
#        strip.show()


# def setNextSeat(start, numPixels):
#    for i in range(start, numPixels):
#        strip.setPixelColor(i, Color(0, 255, 0))
#        strip.setBrightness(255)
#        strip.show()


#  def setSeatInactive(player):
#    inactiveSeat = Seat.findSeat(Character.getCharacterSeat(player))
#    if inactiveSeat is not None:
#        for i in range(inactiveSeat.start, inactiveSeat.length, 1):
#            strip.setPixelColor(i, Color(255, 255, 255))
#            strip.setBrightness(100)
#            strip.show()


# def setAllSeats():
#    for i in range(0, 14, 1):
#            strip.setPixelColor(i, Color(0, 255, 0))
#            strip.setBrightness(100)
#            strip.show()
#    for i in range(14, 91, 1):
#            strip.setPixelColor(i, Color(255, 255, 255))
#            strip.setBrightness(100)
#            strip.show()


def rotatePlayers():
    # TODO

    error = Character.rotatePlayers()
    if not error:
        pass
    else:
        flash(error)
        return


def findPlayer(name):
    for player in players:
        if player.name == name:
            return player
    print("couldn't find player")
    return


def updatePlayers(update_request):
    # if sequence_started:
    #    flash("Cannot sort once sequence has started!")
    #    return

    if(Character.updatePlayers(update_request) == "Error"):
        flash("Must set all initiatives first!")
        return


def resetCharacters():
    global add
    add = ""

    global players
    # players.clear()
    #players = Character.loadCharacters()
    players = Character.query.all()
    print("Players reset")

    # update db
    Character.resetPlayers()

#    setAllSeats()


def checkDex(dex_request):

    rows = Character.query.all()
    list = rows

    for player in rows:
        if "DEX" + player.name in dex_request and player.dexterity == 0:

            for item in list:
                if item.initiative == player.initiative and item.name is not player.name:

                    return player.name
    return None


@index_blueprint.route("/", methods=['GET', 'POST'])
def index():
    resetCharacters()
    return redirect(url_for('index.dashboard'))


@index_blueprint.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    global sequence_started
    if request.method == 'POST':
        if 'button' in request.form:
            if request.form['button'] == 'add_player':
                return redirect(url_for('add_character'))
            elif request.form['button'] == 'save':
                updatePlayers(request.form)
                if checkDex(request.form) is None:
                    pass

            elif request.form['button'] == 'next':
                sequence_started = True
                rotatePlayers()
            elif request.form['button'] == 'reset':
                sequence_started = False
                resetCharacters()
            elif request.form['button'] == 'manage':
                return redirect(url_for('players'))
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
            Character.addMonster()
        elif 'npc' in request.form:
            updatePlayers(request.form)
            # add generic npc
            Character.addNpc()

        #count = len([elem for elem in players if elem.is_player == False])
        #global add
        # if count == 8:
        #   add = "disabled"
        players = Character.query.all()
        # return render_template("dyn.html", content=players, add=add)
        return render_template("dyn.html", content=players, add=add, dex=checkDex(request.form))
    elif request.method == 'GET':
        players = Character.query.all()
        return render_template("dyn.html", content=players, add=add)
