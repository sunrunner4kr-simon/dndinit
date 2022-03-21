from flask import render_template, request, redirect, url_for, flash, Blueprint
from characters import Character
from seats import Seat
from parties import Party
from flask import current_app as app
from rpi_ws281x import Color, PixelStrip, ws
import requests, json
from monsters import Monster


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

def rotatePlayers(party):

    error = Character.rotatePlayers(party)
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


def resetCharacters(party):
    global add
    add = ""

    #global players
    players = Character.query.all()
    print("Players reset")

    # update db
    Character.resetPlayers()
    Party.resetCounts(party)

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
    return redirect(url_for('index.dashboard'))

#@index_blueprint.route('/api/data')
#def data():
#    url = 'https://api.open5e.com/monsters/?format=json&limit=50'
 #   list = requests.get(url)
 #   jsonList = list.json()
 #   return {'data': [monster.to_dict() for monster in jsonList['results']]}

@index_blueprint.route("/add_monster", methods=['GET', 'POST'])
def add_monster():
    if request.method == 'POST':
        if 'back' in request.form:
            return redirect(url_for('index.dashboard'))
        elif 'save' in request.form:
            party = Party.query.filter_by(active=True).first()
            if not party:
                activeParty = 0
                flash("Please select a party first", 'error')
            else:
                activeParty = party.id
                if Character.createPlayer(request.form, activeParty):
                    flash("Character created", 'info')
                else:
                    flash("Character creation failed", 'error')
                return redirect(url_for('index.dashboard'))
    elif request.method == 'GET':
        url = 'https://api.open5e.com/monsters/?format=json&limit=50'
        monsters = requests.get(url)
        x = monsters.json()
        Monster.addMonsters(x)
        monsterList = Monster.query.all()
        return render_template("add_monster.html", content=monsterList)

@index_blueprint.route("/add_character", methods=['GET', 'POST'])
def add_character():
    if request.method == 'POST':
        if 'back' in request.form:
            return redirect(url_for('index.players'))
        elif 'save' in request.form:
            party = Party.query.filter_by(active=True).first()
            if not party:
                activeParty = 0
                flash("Please select a party first", 'error')
            else:
                activeParty = party.id
                if Character.createPlayer(request.form, activeParty):
                    flash("Character created", 'info')
                else:
                    flash("Character creation failed", 'error')
                return redirect(url_for('index.players'))
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
        if 'save' in request.form:
            if Character.updatePlayer(request.form):
                flash("Succesfully saved", 'info')
            #find which party is active
            parties = Party.query.all()
            activeParty = Party.query.filter_by(active=True).first()
            if not activeParty:
                chars = Character.query.all()
            else:
                chars = Character.query.filter_by(party=activeParty.id, is_player=True).all()  
            return render_template("players.html", content=chars, page="players", parties=parties)
        elif 'add_character' in request.form:
            return redirect(url_for('index.add_character'))
        elif 'remove' in request.form:
            # remove player
            if Character.deletePlayer(request.form['remove']):
                flash("Player deleted", 'info')
            else:
                flash("Failed to delete player", 'warning')
        
        if 'changeParty' in request.form:
            Party.toggle_active(request.form['changeParty'])

        #find which party is active
        parties = Party.query.all()
        activeParty = Party.query.filter_by(active=True).first()
        if not activeParty:
            chars = Character.query.all()
        else:
            chars = Character.query.filter_by(party=activeParty.id, is_player=True).all()  
        return render_template("players.html", content=chars, page="players", parties=parties)
    elif request.method == 'GET':
        
        #find which party is active
        parties = Party.query.all()
        activeParty = Party.query.filter_by(active=True).first()
        if not activeParty:
            chars = Character.query.all()
        else:
            chars = Character.query.filter_by(party=activeParty.id, is_player=True).all()
        if not chars:
            flash("No players", 'warning')
        return render_template("players.html", content=chars, page="players", parties=parties)

#TODO: add_seat route

@index_blueprint.route("/seats", methods=['GET', 'POST'])
def seats():
    if request.method == 'POST':
        #TODO: add remove handling
        if 'remove' in request.form:
            if Seat.deleteSeat(request.form):
                flash("Succesfully removed", 'info')
        elif 'save' in request.form:
            if Seat.updateSeat(request.form):
                flash("Succesfully saved", 'info')
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
    party = Party.query.filter_by(active=True).first()
    if not party:
        activeParty = 0
    else:
        activeParty = party.id
    if request.method == 'POST':
        if 'button' in request.form:
            if request.form['button'] == 'save':
                updatePlayers(request.form)
                if checkDex(request.form) is None:
                    pass
            elif request.form['button'] == 'next':
                sequence_started = True
                rotatePlayers(activeParty)
            elif request.form['button'] == 'reset':
                sequence_started = False
                resetCharacters(activeParty)
            elif request.form['button'] == 'manage':
                return redirect(url_for('index.players'))
            elif request.form['button'] == 'seats':
                return redirect(url_for('index.seats'))
            else:
                pass  # unknown
        if 'changeParty' in request.form:
            Party.toggle_active(request.form['changeParty'])
            party = Party.query.filter_by(active=True).first()
            activeParty = party.id
            resetCharacters(activeParty)
        if 'enable' in request.form:
            Character.toggle_enabled(request.form['enable'])
        elif 'remove' in request.form:
            # remove temp player
            if Character.deletePlayer(request.form['remove']):
                flash("Player deleted", 'info')
            else:
                flash("Failed to delete player", 'warning')
            return redirect(url_for('index.dashboard'))

        if 'monster' in request.form:
            updatePlayers(request.form)
            # add generic monster
            return redirect(url_for('index.add_monster'))
            #Character.addMonster(activeParty, party.monster_count)
            #Party.addMonsterCount(activeParty)
        elif 'npc' in request.form:
            updatePlayers(request.form)
            # add generic npc
            Character.addNpc(activeParty, party.npc_count)
            Party.addNpcCount(activeParty)
        elif 'summon' in request.form:
            Character.createSummon(activeParty, request.form['summon'], party.summon_count)
            Party.addSummonCount(activeParty)
        count = Character.query.filter_by(is_player=False).count()
        add = ''
        if count == 7:
            add = "disabled"
        parties = Party.query.all()
        if not activeParty:
            players = Character.query.all()
        else:
            players = Character.query.filter_by(party=activeParty).all()  
        return render_template("dyn.html", content=players, add=add, parties=parties, page="dashboard", dex=checkDex(request.form))
    elif request.method == 'GET':
        add = ''
        count = Character.query.filter_by(is_player=False).count()
        if count == 7:
            add = "disabled"
        parties = Party.query.all()
        if not activeParty:
            players = Character.query.all()
        else:
            print("activeParty is " + str(activeParty))
            players = Character.query.filter_by(party=activeParty).all()        
        return render_template("dyn.html", content=players, add=add, page="dashboard", parties=parties)
