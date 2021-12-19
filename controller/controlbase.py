#! env/bin/python3
from os import getcwd
from sys import path
path.insert(1, getcwd())

from view.viewmenu import VMenu
from view.viewform import VForm
from view.viewform import FormatData

from database.dataplayer import DPlayer
from database.datamatch import DMatch
from database.datatournament import DTournament
from database.dataround import DRound
class ControllerBase:

    def __init__(self, titles):
        self.titles = titles
        self.view_form = VForm(titles)
        self.view_menu = VMenu(titles)

        self.database_player = DPlayer()
        self.database_match = DMatch()
        self.database_tournament = DTournament()
        self.database_round = DRound()


if __name__ == "__main__":
    pass

