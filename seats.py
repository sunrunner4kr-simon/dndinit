from database import db


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
        seat = Seat.query.filter_by(Seat.seat).first()
        return seat
