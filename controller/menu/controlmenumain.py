#! env/bin/python3
""" Main menu controller """
from os import getcwd
from sys import path
path.insert(1, getcwd())

from controller.menu.controlmenubase import ControllerMenuBase 
from controller.menu.controlmenutournament import ControllerMenuTournament 
from controller.menu.controlmenuplayer import ControllerMenuPlayer
from controller.menu.controlmenuhistory import ControllerMenuHistory

from view.viewbase import Title
from view.viewbase import SubtitleLevel


class ControllerMenuMain(ControllerMenuBase):

    def __init__(self, titles):
        super().__init__(titles)
        self.menu_tournament = ControllerMenuTournament(titles)
        self.menu_player = ControllerMenuPlayer(titles)
        self.menu_history = ControllerMenuHistory(titles)

    def show(self):
        
        while True:

            self.titles.clear_subtitle(SubtitleLevel.ALL)
            self.titles.update_subtitle("Menu principal", SubtitleLevel.FIRST)

            my_demands = {1:"Nouveau tournoi",
                          2:"Reprendre tournoi",
                         'a':None,
                          3:"Gestion des joueurs",
                         'b':None,
                          4:"Historique des tournois",
                         'c':None,
                          5:"Quitter"}

            choice = self.view_menu.show_menu(my_demands)

            if choice == 1:
                self.titles.update_subtitle("Création d'un tournoi",
                                            SubtitleLevel.FIRST)
                self.menu_tournament.show_new_tournament()


            elif choice == 2:
                self.titles.update_subtitle("Reprise d'un tournoi",
                                            SubtitleLevel.FIRST)
                self.menu_tournament.show_resume_tournament()

            elif choice == 3:
                self.menu_player.show_menu_player()

            elif choice == 4:
                self.menu_history.show_menu()

            else:
                exit()


if __name__ == "__main__":

    my_titles = Title("GESTIONNAIRE DE TOURNOIS D'ECHECS")
    my_menu = ControllerMenuMain(my_titles)
    my_menu.show()
    
