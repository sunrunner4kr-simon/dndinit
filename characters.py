
class Character:

    def __init__(self, name: str, initiative: int, enabled: bool):
        self.name = name
        self.initiative = initiative
        self.enabled = enabled
        self.is_current = False
        self.is_next = False

    def toggle_enabled(self):
        self.enabled = not self.enabled
