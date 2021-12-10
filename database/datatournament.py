#! env/bin/python3
from os import getcwd
from sys import path
path.insert(1, getcwd())

from database.database import DBase
from model.modeltournament import MTournament


class DTournament(DBase):

    def __init__(self):
        super().__init__("tournaments.json")

    def get_object_by_key(self, key):
        """ Return MTournament object saved in the database with this key """
        my_tournament = MTournament()
        my_tournament.unserialize(super()._dict_by_key(key))
        return my_tournament 

    def get_all_objects(self, sorted_by=["name"]):
        """ Return a list with all tournaments saved
            Sorted with a list of the dictionary's keys """
        dict_list = super()._all_dicts(sorted_by)

        tournaments_list = []
        for elem in dict_list:
            my_tournament = MTournament()
            my_tournament.unserialize(elem)
            tournaments_list.append(my_tournament)
            
        return tournaments_list


if __name__ == "__main__":
    pass

