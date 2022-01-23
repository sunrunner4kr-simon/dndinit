

class character:

    def __init__(self, name, initiative, health, enabled):
        self.name = name
        self.initiative = initiative
        self.health = health
        self.enabled = enabled

    def toggle_enabled(self):
        self.enabled = not self.enabled