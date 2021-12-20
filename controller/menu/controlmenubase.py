#! env/bin/python3
""" Base for menu controllers, regroups main attributes """
from os import getcwd
from sys import path
path.insert(1, getcwd())

from view.viewform import VForm
from view.viewform import FormatData
from view.viewmenu import VMenu

from controller.controltournament import ControllerTournament

class ControllerMenuBase:

    def __init__(self, titles):
        self.titles = titles
        self.view_form = VForm(self.titles)
        self.view_menu = VMenu(self.titles)

        self.controller_tournament = ControllerTournament(self.titles)

