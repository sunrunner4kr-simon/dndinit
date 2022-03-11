import json
from database import db
from seats import Seat


class Character(db.Model):

    name = db.Column(db.String(20), primary_key=True)
    initiative = db.Column(db.Integer, unique=False, nullable=False)
    enabled = db.Column(db.Boolean, unique=False, nullable=False)
    is_current = db.Column(db.Boolean, unique=False, nullable=False)
    is_next = db.Column(db.Boolean, unique=False, nullable=False)
    dexterity = db.Column(db.Integer, unique=False, nullable=False)
    ac = db.Column(db.Integer, unique=False, nullable=False)
    pass_inv = db.Column(db.Integer, unique=False, nullable=False)
    pass_per = db.Column(db.Integer, unique=False, nullable=False)
    is_player = db.Column(db.Boolean, unique=False, nullable=False)
    is_monster = db.Column(db.Boolean, unique=False, nullable=False)
    seat = db.Column(db.Integer, unique=False, nullable=False)

    def __init__(self,
                 name: str,
                 initiative: int,
                 enabled: bool,
                 dexterity: int,
                 ac: int,
                 pass_inv: int,
                 pass_per: int,
                 is_player: bool,
                 is_monster: bool,
                 seat: int
                 ):
        self.name = name
        self.initiative = initiative
        self.enabled = enabled
        self.is_current = False
        self.is_next = False
        self.dexterity = dexterity
        self.ac = ac
        self.pass_inv = pass_inv
        self.pass_per = pass_per
        self.is_player = is_player
        self.is_monster = is_monster
        self.seat = seat

    def getCharacterSeat(playerName):
        char = Character.query.filter_by(name=playerName).first()
        return char.seat

    def toggle_enabled(self):
        player = Character.query.filter_by(name=self.name).first()
        player.enabled = not player.enabled
        db.session.commit()
        self.enabled = not self.enabled

    def addMonster():
        count = Character.query.filter_by(is_monster=True).count()
        monster = Character(
            "Monster " + str(count+1),
            10,
            True,
            0,
            0, 0, 0, False, True, 1)
        db.session.add(monster)
        db.session.commit()

    def addNpc():
        count = Character.query.filter_by(
            is_monster=False, is_player=False).count()
        npc = Character(
            "NPC " + str(count+1),
            10,
            True,
            0,
            0, 0, 0, False, False, 1)
        db.session.add(npc)
        db.session.commit()

    def setSeatInactive(player):
        inactiveSeat = Seat.findSeat(Character.getCharacterSeat(player))
        if inactiveSeat is not None:
            Seat.setSeatInactive(inactiveSeat)


    def resetPlayers():
        rows = Character.query.all()
        for player in rows:
            player.is_current = False
            player.is_next = False
        db.session.commit()

        # delete monsters and npcs
        monsters = Character.query.filter_by(is_player=False).all()
        for monster in monsters:
            db.session.delete(monster)
            db.session.commit()
    
    def createPlayer(create_request):
        new = Character(
            create_request['name-input'],
            create_request['initiative-input'],
            True,
            create_request['dexterity-input'],
            0, 0, 0, True, False, create_request['seat-input'])
        db.session.add(new)
        db.session.commit()

    def updatePlayers(update_request):
        rows = Character.query.all()
        for row in rows:
            if row.name in update_request:
                if not update_request[row.name]:
                    return "Error"
                sep = ' '
                stripped = update_request[row.name].split(sep, 1)[0]
                row.initiative = int(stripped)
            if "DEX" + row.name in update_request:
                row.dexterity = int(update_request["DEX"+row.name])
                print(row.name + " dex updated to " +
                      update_request["DEX"+row.name])
        db.session.commit()

    def updatePlayer(update_request):
        char = Character.query.filter_by(name=update_request['save']).first()
        print("updating: " + update_request['save'])
        if not char:
            return False
        else:
            char.dexterity = update_request['dexterity']
            char.ac = update_request['ac']
            char.pass_per = update_request['per']
            char.pass_inv = update_request['inv']
            char.seat = update_request['seat']
            print(char.name + " updated" )
            db.session.commit()
            return True

    def getNextActivePlayer(players):
        for char in players:
            if char.is_next:
                return char
        return

    def getCurrentActivePlayer(players):
        if len(players) < 2:
            return
        char = Character.query.filter_by(is_current=True).first()
        if not char:
            return None
        else:
            return char

    def findNextEnabledPlayer(start_index, players):
        if start_index >= len(players):
            start_index = 0
        for i in range(start_index, len(players)):
            if players[i].enabled and not players[i].is_current and not players[i].is_next:
                return players[i]

        for i in range(0, start_index):
            if players[i].enabled and not players[i].is_current and not players[i].is_next:
                return players[i]

    def rotatePlayers():
        # TODO
        rows = Character.query.order_by(
            Character.initiative.desc(), Character.dexterity.desc()).all()
        enabled_player_count = 0
        for player in rows:
            if player.enabled:
                enabled_player_count = enabled_player_count + 1

        if enabled_player_count < 3:
            return "Not enough enabled players!"

        if Character.getCurrentActivePlayer(rows) is None:
            currentPlayer = Character.findNextEnabledPlayer(0, rows)
            currentPlayer.is_current = True

            nextPlayer = Character.findNextEnabledPlayer(0, rows)
            nextPlayer.is_next = True
            db.session.commit()
            # Get seat details for player seat
            newseat = Seat.findSeat(currentPlayer.seat)
            if newseat is not None:
                Seat.setCurrentSeat(newseat.start, newseat.length)
            if newseat is not Seat.findSeat(nextPlayer.seat):
                newseat = Seat.findSeat(nextPlayer.seat)
                if newseat is not None:
                    Seat.setNextSeat(newseat.start, newseat.length)
        else:
            # Current player is no longer current, moved to what was previously next player
            currentPlayer = Character.getCurrentActivePlayer(rows)
            currentPlayer.is_current = False

            print("Setting last current false: " + currentPlayer.name)
            # set white
            Character.setSeatInactive(currentPlayer.name)
            next_player = Character.getNextActivePlayer(rows)
            next_player.is_current = True
            print("Setting new current true: " + next_player.name)
            next_player.is_next = False
            print("Setting new current next false: " + next_player.name)
            nextSeat = Seat.findSeat(next_player.seat)
            Seat.setCurrentSeat(nextSeat.start, nextSeat.length)
            print("Set Current Seat: " + next_player.name)
            db.session.commit()
            # New next player found here
            nextPlayer = Character.findNextEnabledPlayer(
                rows.index(next_player), rows)
            nextPlayer.is_next = True
            print("Setting new next true: " + nextPlayer.name)
            db.session.commit()
            if Seat.findSeat(next_player.seat) is not Seat.findSeat(nextPlayer.seat):
                Seat.setNextSeat(Seat.findSeat(nextPlayer.seat).start, Seat.findSeat(nextPlayer.seat).length)
                print("Set Next Seat: " + nextPlayer.name)

    def savePlayer(update):
        players = []
        # Opening JSON file
        f = open('players.json')

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
        # Closing file
        f.close()

        # make updates

        # save again
        json_string = json.dumps([Character.__dict__ for Character in players])
        print(json_string)
        with open("players.json", "w") as outfile:
            json.dump(json_string, outfile)

        return players