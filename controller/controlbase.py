#! env/bin/python3
""" Base for controllers, regroups main attributes """
from os import getcwd
from sys import path
path.insert(1, getcwd())

from view.viewmenu import VMenu
from view.viewform import VForm


class ControllerBase:

    def __init__(self, titles):
        self.titles = titles
        self.view_form = VForm(titles)
        self.view_menu = VMenu(titles)
