
class Character:

    def __init__(self,
                 name: str,
                 initiative: int,
                 enabled: bool,
                 dexterity: int,
                 ac: int,
                 pass_int: int,
                 pass_per: int,
                 is_player: bool
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

    def toggle_enabled(self):
        self.enabled = not self.enabled
