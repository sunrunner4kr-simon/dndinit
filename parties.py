from database import db
from flask import current_app as app
from rpi_ws281x import Color, PixelStrip, ws

class Party(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    active = db.Column(db.Boolean, unique=False, nullable=False )

    def __init__(self,
                 name: str,
                 active: bool):
        self.name = name
        self.active = active
    
    def toggle_active(partyName):
        oldActiveParty = Party.query.filter_by(active=True).first()
        if not oldActiveParty:
            pass
        else:
            oldActiveParty.active = False
        newActiveParty = Party.query.filter_by(name=partyName).first()
        newActiveParty.active = True
        db.session.commit()

    def createParty(create_request):
        new = Party(
            name=create_request['name-input'],
            active=False)
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
    
    def deleteParty(update_request):
        party = Party.query.filter_by(id=update_request['remove']).first()
        if not party:
            return False
        else:
            db.session.delete(party)
            db.session.commit()
            return True
