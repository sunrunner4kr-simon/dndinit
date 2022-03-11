from database import db
from flask import current_app as app
from rpi_ws281x import Color, PixelStrip, ws

class Party(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)

    def __init__(self,
                 name: str):
        self.name = name

    def createParty(create_request):
        new = Party(
            name=create_request['name-input'])
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
