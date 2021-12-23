#! env/bin/python3
""" Database for players """
from os import getcwd
from sys import path
path.insert(1, getcwd())

from database.database import DBase
from model.modelplayer import MPlayer


class DPlayer(DBase):
    """ Database for players, create the file and specialised class
        for MPlayer """

    def __init__(self):
        super().__init__("players.json")

    def get_object_by_key(self, key):
        """ Return MPlayer object saved in the database with this key """
        my_player = MPlayer()
        my_player.unserialize(super()._dict_by_key(key))
        return my_player

    def get_all_objects(self):
        """ Return the list of all MPlayer saved in database """

        players_list = []
        for elem in self.data_base.all():
            my_player = MPlayer()
            my_player.unserialize(elem)
            players_list.append(my_player)

        return players_list
