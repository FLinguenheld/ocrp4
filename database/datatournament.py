#! env/bin/python3
""" Database for tournaments """
from os import getcwd
from sys import path
path.insert(1, getcwd())

from database.database import DBase
from model.modeltournament import MTournament


class DTournament(DBase):
    """ Database for tournaments, create the file and specialised class
        for MTournament """

    def __init__(self):
        super().__init__("tournaments.json")

    def get_object_by_key(self, key):
        """ Return MTournament object saved in the database with this key """
        my_tournament = MTournament()
        my_tournament.unserialize(super()._dict_by_key(key))
        return my_tournament

    def get_all_objects(self):
        """ Return the list of all MTournament saved in database """

        tournaments_list = []
        for elem in self.data_base.all():
            my_tournament = MTournament()
            my_tournament.unserialize(elem)
            tournaments_list.append(my_tournament)

        return tournaments_list


if __name__ == "__main__":
    pass
