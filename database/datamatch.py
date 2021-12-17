#! env/bin/python3
from os import getcwd
from sys import path
path.insert(1, getcwd())

from database.database import DBase
from model.modelmatch import MMatch 


class DMatch(DBase):

    def __init__(self):
        super().__init__("matchs.json")

    def get_object_by_key(self, key):
        """ Return MMatch object saved in the database with this key """
        my_match = MMatch()
        my_match.unserialize(super()._dict_by_key(key))
        return my_match

    def get_objects_by_keys(self, list_of_keys):
        """ Return matches from the round_object given """
        my_matches = []
        for k in list_of_keys:
            my_matches.append(self.get_object_by_key(k))

        return my_matches


if __name__ == "__main__":
    pass

