from flask import render_template, request, redirect, url_for, flash, Blueprint
from characters import Character
from seats import Seat
from parties import Party
from flask import current_app as app
from rpi_ws281x import Color, PixelStrip, ws


index_blueprint = Blueprint('index', __name__)

sequence_started = False

add = ""

def setSeatInactive(player):
    inactiveSeat = Seat.findSeat(Character.getCharacterSeat(player))
    if inactiveSeat is not None:
        Seat.setSeatInactive(inactiveSeat)


def setAllSeats():
    for i in range(0, 14, 1):
            app.strip.setPixelColor(i, Color(0, 255, 0))
            app.strip.setBrightness(100)
            app.strip.show()
    for i in range(14, 91, 1):
            app.strip.setPixelColor(i, Color(255, 255, 255))
            app.strip.setBrightness(100)
            app.strip.show()

def rotatePlayers():
    # TODO

    error = Character.rotatePlayers()
    if not error:
        pass
    else:
        flash(error)
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

    #global players
    players = Character.query.all()
    print("Players reset")

    # update db
    Character.resetPlayers()

    setAllSeats()


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

@index_blueprint.route("/add_character", methods=['GET', 'POST'])
def add_character():
    if request.method == 'POST':
        if 'back' in request.form:
            return redirect(url_for('index.dashboard'))
        elif 'save' in request.form:
            if Character.createPlayer(request.form):
                flash("Character created", 'info')
            else:
                flash("Character creation failed", 'error')
        
        return redirect(url_for('index.dashboard'))
    elif request.method == 'GET':
        return render_template("add_characters.html")

@index_blueprint.route("/add_party", methods=['GET', 'POST'])
def add_party():
    if request.method == 'POST':
        if 'back' in request.form:
            return redirect(url_for('index.parties'))
        elif 'save' in request.form:
            if Party.createParty(request.form):
                flash("Party created", 'info')
            else:
                flash("Party creation failed", 'error')
        
        return redirect(url_for('index.parties'))
    elif request.method == 'GET':
        return render_template("add_party.html")

@index_blueprint.route("/players", methods=['GET', 'POST'])
def players():
    if request.method == 'POST':
        #TODO: add remove handling
        if 'save' in request.form:
            if Character.updatePlayer(request.form):
                flash("Succesfully saved", 'info')
            chars = Character.query.filter_by(is_player=True).all()
            return render_template("players.html", content=chars, page="players")
        elif 'add_character' in request.form:
            return redirect(url_for('index.add_character'))

        chars = Character.query.filter_by(is_player=True).all()
        return render_template("players.html", content=chars, page="players")
    elif request.method == 'GET':
        chars = Character.query.filter_by(is_player=True).all()
        if not chars:
            flash("No players", 'warning')
        return render_template("players.html", content=chars, page="players")

@index_blueprint.route("/seats", methods=['GET', 'POST'])
def seats():
    if request.method == 'POST':
        #TODO: add remove handling
        #TODO: add save handling
        
        seats = Seat.query.all()
        return render_template("seats.html", content=seats, page="seats")
    elif request.method == 'GET':
        seats = Seat.query.all()
        return render_template("seats.html", content=seats, page="seats")

@index_blueprint.route("/parties", methods=['GET', 'POST'])
def parties():
    if request.method == 'POST':
        if 'remove' in request.form:
            if Party.deleteParty(request.form):
                flash("Succesfully removed", 'info')
        elif 'save' in request.form:
            if Party.updateParty(request.form):
                flash("Succesfully saved", 'info')
        elif 'add_party' in request.form:
            return redirect(url_for('index.add_party'))
        parties = Party.query.all()
        return render_template("parties.html", content=parties, page="parties")
    elif request.method == 'GET':
        parties = Party.query.all()
        return render_template("parties.html", content=parties, page="parties")

@index_blueprint.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    global sequence_started
    if request.method == 'POST':
        if 'button' in request.form:
            if request.form['button'] == 'save':
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
                return redirect(url_for('index.players'))
            elif request.form['button'] == 'seats':
                return redirect(url_for('index.seats'))
            else:
                pass  # unknown
        if 'enable' in request.form:
            Character.toggle_enabled(request.form['enable'])
        elif 'remove' in request.form:
            # remove temp player
            if Character.deletePlayer(request.form['remove']):
                flash("Player deleted", 'info')
            else:
                flash("Failed to delete player", 'warning')
            return redirect(url_for('index.dashboard'))
        elif 'monster' in request.form:
            updatePlayers(request.form)
            # add generic monster
            Character.addMonster()
        elif 'npc' in request.form:
            updatePlayers(request.form)
            # add generic npc
            Character.addNpc()

        count = Character.query.filter_by(is_player=False).count()
        add = ''
        if count == 7:
            add = "disabled"
        players = Character.query.all()
        return render_template("dyn.html", content=players, add=add, page="dashboard", dex=checkDex(request.form))
    elif request.method == 'GET':
        add = ''
        count = Character.query.filter_by(is_player=False).count()
        if count == 7:
            add = "disabled"
        players = Character.query.all()
        return render_template("dyn.html", content=players, add=add, page="dashboard")
