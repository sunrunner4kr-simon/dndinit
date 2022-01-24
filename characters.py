
class Character:

    def __init__(self, name: str, initiative: int, health: int, enabled: bool):
        self.name = name
        self.initiative = initiative
        self.health = health
        self.enabled = enabled

    def toggle_enabled(self):
        self.enabled = not self.enabled
