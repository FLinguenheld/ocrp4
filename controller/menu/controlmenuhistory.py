#! env/bin/python3
""" Menu controller hitory """
from os import getcwd
from sys import path
path.insert(1, getcwd())

from operator import attrgetter

from controller.menu.controlmenubase import ControllerMenuBase
from view.viewbase import SubtitleLevel

from database.datatournament import DTournament
from controller.controltournament import ControllerTournament


class ControllerMenuHistory(ControllerMenuBase):
    """ Regroup menus to manage the history """

    def __init__(self, titles):
        super().__init__(titles)
        self.controller_tournament = ControllerTournament(titles)

    def show_menu(self):

        tournaments = DTournament().get_all_objects()

        while True:

            self.titles.clear_subtitle(SubtitleLevel.ALL)
            self.titles.update_subtitle("Historique", SubtitleLevel.FIRST)

            my_demands = {1: "Selection tournoi par nom",
                          2: "Selection tournoi par ville",
                          3: "Sélection tournoi par date",
                          'a': None,
                          4: "Quitter"}

            choice = self.view_menu.show_menu(my_demands)

            if choice == 1:
                self.titles.update_subtitle("Selectionner un tournoi (liste par nom)",
                                            SubtitleLevel.SECOND)

                tournaments.sort(key=lambda k: k.name.lower(), reverse=False)
                self._ask_and_show(tournaments)

            elif choice == 2:
                self.titles.update_subtitle("Selectionner un tournoi (liste par ville)",
                                            SubtitleLevel.SECOND)

                tournaments.sort(key=lambda k: k.place.lower(), reverse=False)
                self._ask_and_show(tournaments)

            elif choice == 3:
                self.titles.update_subtitle("Selectionner un tournoi (liste par date)",
                                            SubtitleLevel.SECOND)

                tournaments.sort(key=attrgetter("date"), reverse=True)
                self._ask_and_show(tournaments)

            else:
                return None

    def _ask_and_show(self, tournaments):
        """ Show tournaments and ask to select one.
            Print the abstract """
        if DTournament().get_all_objects():
            tournament_selected = self.controller_tournament.selection_tournament(tournaments)
            self.controller_tournament.abstract_tournament(tournament_selected)
        else:

            self.titles.update_subtitle("Aucun tournoi existant", SubtitleLevel.SECOND)
            self.view_menu.print_titles()
            self.view_menu.print_line_break()
            self.view_menu.print_text("Aucune donnée à afficher")
