#! env/bin/python3
""" Database for rounds """
from os import getcwd
from sys import path
path.insert(1, getcwd())

from database.database import DBase
from model.modelround import MRound


class DRound(DBase):
    """ Database for rounds, create the file and specialised class for MRound """

    def __init__(self):
        super().__init__("rounds.json")

    def get_object_by_key(self, key):
        """ Return MRound object saved in the database with this key """
        my_round = MRound()
        my_round.unserialize(super()._dict_by_key(key))
        return my_round


if __name__ == "__main__":
    pass
