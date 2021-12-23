#! env/bin/python4
""" Main of chessManager. Creates the title and launches the main menu """
from controller.menu.controlmenumain import ControllerMenuMain
from view.title import Title
from view.viewmenu import VMenu

my_titles = Title("GESTIONNAIRE DE TOURNOIS D'ECHECS", line_length=100)
my_view = VMenu(my_titles)
my_menu = ControllerMenuMain(my_titles)
my_menu.show()
