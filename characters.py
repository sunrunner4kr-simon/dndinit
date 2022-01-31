import json


class Character:

    def __init__(self,
                 name: str,
                 initiative: int,
                 enabled: bool,
                 dexterity: int,
                 ac: int,
                 pass_int: int,
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
        self.pass_int = pass_int
        self.pass_per = pass_per
        self.is_player = is_player
        self.is_monster = is_monster
        self.seat = seat

    def toggle_enabled(self):
        self.enabled = not self.enabled

    def loadCharacters():
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
        return players
