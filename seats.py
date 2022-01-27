class Seat:

    def __init__(self,
                 seat: int,
                 start: int,
                 length: int):
        self.seat = seat
        self.start = start
        self.length = length
        
    def setupSeats():
        
      import json

      # Opening JSON file
      f = open('seats.json')

      # returns JSON object as
      # a dictionary
      data = json.load(f)

      # Iterating through the json
      # list
      seats = []
      for i in data['seats']:
          
          seats.append(Seat(
                int(i['seat']),
                int(i['start']),
                int(i['length'])))
      print(seats)
      # Closing file
      f.close()
      return seats


