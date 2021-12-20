#! env/bin/python3
""" Main menu controller """
from os import getcwd
from sys import path
path.insert(1, getcwd())

from controller.menu.controlmenubase import ControllerMenuBase 
from controller.menu.controlmenutournament import ControllerMenuTournament 

from controller.controlplayer import ControllerPlayer
from view.viewbase import Title
from view.viewbase import SubtitleLevel


class ControllerMenuMain(ControllerMenuBase):

    def __init__(self, titles):
        super().__init__(titles)
        self.menu_tournament = ControllerMenuTournament(titles)

    def show(self):
        
        while True:

            self.titles.clear_subtitle(SubtitleLevel.ALL)
            self.titles.update_subtitle("Menu principal", SubtitleLevel.FIRST)

            my_demands = {1:"Nouveau tournoi",
                          2:"Reprendre tournoi",
                         'a':None,
                          3:"Nouveau joueur",
                          4:"Liste des joueurs",
                         'b':None,
                          5:"Rapports",
                         'c':None,
                          6:"Quitter"}

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
                self.titles.update_subtitle("Création d'un nouveau joueur",
                                            SubtitleLevel.FIRST)
                controller_player = ControllerPlayer(self.titles)
                controller_player.create_player()

            elif choice == 4:
                self.titles.update_subtitle("Liste des joueurs",
                                            SubtitleLevel.FIRST)
                controller_player = ControllerPlayer(self.titles)
                controller_player.list_players()


            elif choice == 5:
                pass


            else:
                exit()

if __name__ == "__main__":

    my_titles = Title("GESTIONNAIRE DE TOURNOIS D'ECHECS")
    my_menu = ControllerMenuMain(my_titles)
    my_menu.show()
    
