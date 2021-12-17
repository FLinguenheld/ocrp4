#! env/bin/python3
from os import getcwd
from sys import path
path.insert(1, getcwd())

from model.modelbase import MBase


class MMatch(MBase):

    def __init__(self, key=0, player_keys=[], winner=None):
        super().__init__(key, "")
        self.player_keys = player_keys
        self.winner = winner

    def __str__(self):
        return f" player_keys : {self.player_keys}"\
        f" winner : {self.winner}"

    def __repr__(self):
        return f"Match:"\
        f" key : {self.key}"\
        f" player_keys : {self.player_keys}"\
        f" winner : {self.winner}"

    def serialize(self):
        dict_to_serialize = super().serialize()
        dict_to_serialize["player_keys"] = self.player_keys
        dict_to_serialize["winner"] = self.winner

        return dict_to_serialize

    def unserialize(self, values):
        super().unserialize(values)
        self.player_keys = values["player_keys"]
        self.winner = values["winner"]

    def __eq__(self, other_match):
        """ Compare the players of two matches """ 
        return sorted(self.player_keys) == sorted(other_player.player_keys)


if __name__ == "__main__":
    my_match = MMatch(2415, [1021, 98543])
    print(my_match)

