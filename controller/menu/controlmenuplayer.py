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
        """ Show the menu player to manage and list the players in database """

        while True:

            self.titles.clear_subtitle(SubtitleLevel.ALL)
            self.titles.update_subtitle("Gestion des joueurs", SubtitleLevel.FIRST)

            my_demands = {1: "Nouveau joueur",
                          2: "Modifier joueur",
                          3: "Mettre à jour le classement ELO",
                          'a': None,
                          4: "Liste des joueurs par classement",
                          5: "Liste des joueurs par nom",
                          6: "Liste des joueurs par prénom",
                          'b': None,
                          7: "Quitter"}

            choice = self.view_menu.show_menu(my_demands)

            if choice == 1:
                self.titles.update_subtitle("Création d'un nouveau joueur",
                                            SubtitleLevel.SECOND)

                self.controller_player.create_player()

            elif choice == 7:
                return None

            elif self._check_if_players():

                if choice == 2:
                    self.titles.update_subtitle("Modification d'un joueur",
                                                SubtitleLevel.SECOND)

                    # Select a player
                    player_key = self.controller_player.selection_player(number=1)
                    selected_player = DPlayer().get_object_by_key(player_key)

                    # Update
                    self.controller_player.update_player(selected_player)

                elif choice == 3:
                    self.titles.update_subtitle("Modification du classement ELO",
                                                SubtitleLevel.SECOND)
                    self._update_elo()

                elif choice == 4:
                    self.titles.update_subtitle("Liste des joueurs par classement",
                                                SubtitleLevel.SECOND)

                    players = DPlayer().get_all_objects()
                    players.sort(key=lambda k: k.last_name.lower(), reverse=False)
                    players.sort(key=lambda k: k.name.lower(), reverse=False)
                    players.sort(key=attrgetter("rank"), reverse=True)

                    self._show_list(players)

                elif choice == 5:
                    self.titles.update_subtitle("Liste des joueurs par nom",
                                                SubtitleLevel.SECOND)

                    players = DPlayer().get_all_objects()
                    players.sort(key=attrgetter("rank"), reverse=True)
                    players.sort(key=lambda k: k.name.lower(), reverse=False)
                    players.sort(key=lambda k: k.last_name.lower(), reverse=False)

                    self._show_list(players)

                elif choice == 6:
                    self.titles.update_subtitle("Liste des joueurs par prénom",
                                                SubtitleLevel.SECOND)

                    players = DPlayer().get_all_objects()
                    players.sort(key=attrgetter("rank"), reverse=True)
                    players.sort(key=lambda k: k.last_name.lower(), reverse=False)
                    players.sort(key=lambda k: k.name.lower(), reverse=False)

                    self._show_list(players)

    def _show_list(self, players):
        """ Print titles and list given """

        self.view_form.print_titles(True)
        self.view_form.print_line_break()

        text = str()
        for p in players:
            text += f"{p}\n"

        self.view_form.print_text(text, ask_to_continue=True, center=True)

    def _update_elo(self):
        """ Allows to update a user's rank, shows a page to select a player
            and update in database """

        player_key = self.controller_player.selection_player(number=1)
        player = DPlayer().get_object_by_key(player_key)

        # Form
        my_demand = {"elo": {"name": f"Nouveau classement ELo de {player.complete_name}",
                             "format": FormatData.UINT,
                             "value": player.rank}}

        my_demand = self.view_form.show_form(my_demand)

        # Update player and save
        player.rank = my_demand["elo"]["value"]
        DPlayer().update_object(player)

    def _check_if_players(self):
        """ Check if there is at least one player in database.
            Otherwise, show a message."""

        if DPlayer().get_all_objects():
            return True
        else:
            self.titles.update_subtitle("Aucun joueur existant", SubtitleLevel.SECOND)
            self.view_menu.print_titles()
            self.view_menu.print_line_break()
            self.view_menu.print_text("Aucune donnée à afficher")
            return False
