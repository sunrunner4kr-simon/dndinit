import json


class CharacterManager:

    def __init__(self, lst):
        self._lst = lst

    def __getitem__(self, item):
        return self._lst[item]
