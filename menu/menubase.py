#! env/bin/python3
from os import getcwd
from sys import path
path.insert(1, getcwd())

from view.viewform import VForm
from view.viewform import FormatData
from view.viewmenu import VMenu

from database.dataplayer import DPlayer
from database.datamatch import DMatch
from database.datatournament import DTournament

class MenuBase:

    def __init__(self):
        self.titles = ["GESTIONNAIRE DE TOURNOI D'ECHECS"]
        self.view_form = VForm(self.titles)
        self.view_menu = VMenu(self.titles)

        self.database_player = DPlayer()
        self.database_match = DMatch()
        self.database_tournament = DTournament()


if __name__ == "__main__":
    pass

