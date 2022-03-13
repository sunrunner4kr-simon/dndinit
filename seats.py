from database import db
from flask import current_app as app
from rpi_ws281x import Color, PixelStrip, ws

class Seat(db.Model):

    seat = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.Integer, unique=False, nullable=False)
    length = db.Column(db.Integer, unique=False, nullable=False)

    def __init__(self,
                 seat: int,
                 start: int,
                 length: int):
        self.seat = seat
        self.start = start
        self.length = length

    def findSeat(seatNumber):
        seat = Seat.query.filter_by(seat=Seat.seat).first()
        return seat

    def setNextSeat(start, numPixels):
        for i in range(start, numPixels):
            app.strip.setPixelColor(i, Color(0, 255, 0))
            app.strip.setBrightness(255)
            app.strip.show()

    def setSeatInactive(inactiveSeat):
        for i in range(inactiveSeat.start, inactiveSeat.length, 1):
            app.strip.setPixelColor(i, Color(255, 255, 255))
            app.strip.setBrightness(100)
            app.strip.show()

    def setCurrentSeat(start, numPixels):
        for i in range(start, numPixels):
            app.strip.setPixelColor(i, Color(255, 0, 0))
            app.strip.setBrightness(255)
            app.strip.show()
    
    def updateSeat(update_request):
        seat = Seat.query.filter_by(seat=update_request['save']).first()
        if not seat:
            return False
        else:
            seat.start = update_request['start']
            seat.length = update_request['length']
            print(str(seat.seat) + " updated" )
            db.session.commit()
            return True
    
    def deleteSeat(update_request):
        seat = Seat.query.filter_by(seat=update_request['remove']).first()
        if not seat:
            return False
        else:
            db.session.delete(seat)
            db.session.commit()
            return True
