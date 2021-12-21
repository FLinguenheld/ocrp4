#! env/bin/python3
""" Menu controller for players in main menu """
from os import getcwd
from sys import path
path.insert(1, getcwd())

from operator import attrgetter

from controller.menu.controlmenubase import ControllerMenuBase
from controller.controlplayer import ControllerPlayer

from view.viewbase import SubtitleLevel
from view.viewform import FormatData

from database.dataplayer import DPlayer

class ControllerMenuPlayer(ControllerMenuBase):

    def __init__(self, titles):
        super().__init__(titles)
        self.controller_player = ControllerPlayer(self.titles)

    def show_menu_player(self):
        """"  """ 

        while True:

            self.titles.clear_subtitle(SubtitleLevel.ALL)
            self.titles.update_subtitle("Gestion des joueurs", SubtitleLevel.FIRST)

            my_demands = {1:"Nouveau joueur",
                          2:"Mettre à jour le classement ELO",
                         'a':None,
                          3:"Liste des joueurs par classement",
                          4:"Liste des joueurs par nom",
                          5:"Liste des joueurs par prénom",
                         'b':None,
                          6:"Quitter"}

            choice = self.view_menu.show_menu(my_demands)

            if choice == 1:
                self.titles.update_subtitle("Création d'un nouveau joueur",
                                            SubtitleLevel.SECOND)
                self.controller_player.create_player()

            elif choice == 2:
                self._update_elo()

            elif choice == 3:
                self.titles.update_subtitle("Liste des joueurs par classement",
                                            SubtitleLevel.SECOND)

                players = DPlayer().get_all_objects()
                players.sort(key=attrgetter("name", "last_name"))
                players.sort(key=attrgetter("rank"), reverse=True)

                self._show_list(players)

            elif choice == 4:
                self.titles.update_subtitle("Liste des joueurs par nom",
                                            SubtitleLevel.SECOND)

                players = DPlayer().get_all_objects()
                players.sort(key=attrgetter("rank"), reverse=True)
                players.sort(key=attrgetter("last_name", "name"))

                self._show_list(players)

            elif choice == 5:
                self.titles.update_subtitle("Liste des joueurs par prénom",
                                            SubtitleLevel.SECOND)

                players = DPlayer().get_all_objects()
                players.sort(key=attrgetter("rank"), reverse=True)
                players.sort(key=attrgetter("name", "last_name"))

                self._show_list(players)

            else:
                return None

    def _show_list(self, players):
        """ Print titles and list given """
        text = "\n"
        for p in players:
            text += f" - {p}\n"

        self.view_form.print_titles(True)
        self.view_form.print_text(text)

    def _update_elo(self):
        
        player_key = self.controller_player.selection_player(number=1)
        player = DPlayer().get_object_by_key(player_key)

        # Form
        my_demand = {"elo" : {"name" : f"Nouveau classement ELo de {player.complete_name}",
                              "format" : FormatData.UINT,
                              "value" : player.rank}}

        my_demand = self.view_form.show_form(my_demand)

        # Update player and save
        player.rank = my_demand["elo"]["value"]
        DPlayer().update_object(player)



