from database import db
from flask import current_app as app
from rpi_ws281x import Color, PixelStrip, ws

class Party(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    active = db.Column(db.Boolean, unique=False, nullable=False )
    monster_count = db.Column(db.Integer, unique=False, nullable=False)
    npc_count = db.Column(db.Integer, unique=False, nullable=False)
    summon_count = db.Column(db.Integer, unique=False, nullable=False)

    def __init__(self,
                 name: str,
                 active: bool,
                 monster_count: int,
                 npc_count: int,
                 summon_count: int):
        self.name = name
        self.active = active
        self.monster_count = monster_count
        self.npc_count = npc_count
        self.summon_count = summon_count

    def resetCounts(partyId):
        party = Party.query.filter_by(id=partyId).first()
        if not party:
            pass
        else:
            party.monster_count=0
            party.npc_count=0
            party.summon_count=0
            db.session.commit()
    
    def toggle_active(partyName):
        oldActiveParty = Party.query.filter_by(active=True).first()
        if not oldActiveParty:
            pass
        else:
            oldActiveParty.active = False
        newActiveParty = Party.query.filter_by(name=partyName).first()
        newActiveParty.active = True
        db.session.commit()

    def addMonsterCount(partyId):
        party = Party.query.filter_by(id=partyId).first()
        if not party:
            pass
        else:
            party.monster_count+=1
            db.session.commit()

    def addNpcCount(partyId):
        party = Party.query.filter_by(id=partyId).first()
        if not party:
            pass
        else:
            party.npc_count+=1
            db.session.commit()

    def addSummonCount(partyId):
        party = Party.query.filter_by(id=partyId).first()
        if not party:
            pass
        else:
            party.summon_count+=1
            db.session.commit()

    def createParty(create_request):
        new = Party(
            name=create_request['name-input'],
            active=False,
            monster_count=0,
            npc_count=0,
            summon_count=0)
        db.session.add(new)
        db.session.commit()

    def updateParty(update_request):
        party = Party.query.filter_by(id=update_request['save']).first()
        if not party:
            return False
        else:
            party.name = update_request['name']
            print(party.name + " updated" )
            db.session.commit()
            return True
    
    #TODO: can't remove if players attached
    def deleteParty(update_request):
        party = Party.query.filter_by(id=update_request['remove']).first()
        if not party:
            return False
        else:
            db.session.delete(party)
            db.session.commit()
            return True
