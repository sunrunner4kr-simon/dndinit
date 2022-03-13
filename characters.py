import json
from database import db
from seats import Seat


class Character(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
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
    party = db.Column(db.Integer, unique=False, nullable=False)

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
                 seat: int,
                 party: int
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
        self.party = party

    def getCharacterSeat(playerName):
        char = Character.query.filter_by(name=playerName).first()
        return char.seat

    def toggle_enabled(playerName):
        player = Character.query.filter_by(name=playerName).first()
        player.enabled = not player.enabled
        db.session.commit()

    def addMonster(party, count):
        monster = Character(
            "Monster " + str(count+1),
            10,
            True,
            0,
            0, 0, 0, False, True, 1, party)
        db.session.add(monster)
        db.session.commit()

    def createSummon(party, playerName, count):
        player = Character.query.filter_by(name=playerName).first()
        if not player:
            return False

        monster = Character(
            "Summon " + str(count+1),
            10,
            True,
            0,
            0, 0, 0, False, True, player.seat, party)
        db.session.add(monster)
        db.session.commit()

    def addNpc(party, count):
        npc = Character(
            "NPC " + str(count+1),
            10,
            True,
            0,
            0, 0, 0, False, False, 1, party)
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
    
    def createPlayer(create_request, party):
        new = Character(
            create_request['name-input'],
            create_request['initiative-input'],
            True,
            create_request['dexterity-input'],
            0, 0, 0, True, False, create_request['seat-input'], party)
        db.session.add(new)
        db.session.commit()

    def deletePlayer(playerName):
        char = Character.query.filter_by(name=playerName).first()
        if not char:
            return False
        else:
            db.session.delete(char)
            db.session.commit()    
            return True

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
            char.name = update_request['name']
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

    def findNextEnabledPlayer(start_index, players, party):
        if start_index >= len(players):
            start_index = 0
        for i in range(start_index, len(players)):
            if players[i].enabled and players[i].party == party and not players[i].is_current and not players[i].is_next:
                return players[i]

        for i in range(0, start_index):
            if players[i].enabled and players[i].party == party and not players[i].is_current and not players[i].is_next:
                return players[i]

    def rotatePlayers(party):
        rows = Character.query.order_by(
            Character.initiative.desc(), Character.dexterity.desc()).all()
        enabled_player_count = 0
        for player in rows:
            if player.enabled:
                enabled_player_count = enabled_player_count + 1

        if enabled_player_count < 3:
            return "Not enough enabled players!"

        if Character.getCurrentActivePlayer(rows) is None:
            currentPlayer = Character.findNextEnabledPlayer(0, rows, party)
            currentPlayer.is_current = True

            nextPlayer = Character.findNextEnabledPlayer(0, rows, party)
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
                rows.index(next_player), rows, party)
            nextPlayer.is_next = True
            print("Setting new next true: " + nextPlayer.name)
            db.session.commit()
            if Seat.findSeat(next_player.seat) is not Seat.findSeat(nextPlayer.seat):
                Seat.setNextSeat(Seat.findSeat(nextPlayer.seat).start, Seat.findSeat(nextPlayer.seat).length)
                print("Set Next Seat: " + nextPlayer.name)