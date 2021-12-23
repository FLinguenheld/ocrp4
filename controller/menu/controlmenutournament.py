#! env/bin/python3
""" Menu controller for tournaments """
from os import getcwd
from sys import path
path.insert(1, getcwd())

from operator import attrgetter

from controller.menu.controlmenubase import ControllerMenuBase
from controller.menu.controlmenuround import ControllerMenuRound

from controller.controltournament import ControllerTournament
from controller.controlplayer import ControllerPlayer
from controller.controlround import ControllerRound

from view.viewbase import SubtitleLevel

from database.datatournament import DTournament
from database.dataround import DRound
from database.dataplayer import DPlayer


class ControllerMenuTournament(ControllerMenuBase):
    """ Regroup menus to manage the tournaments """

    def __init__(self, titles):
        super().__init__(titles)
        self.controller_tournament = ControllerTournament(self.titles)
        self.controller_player = ControllerPlayer(self.titles)
        self.controller_round = ControllerRound(self.titles)
        self.menu_round = ControllerMenuRound(self.titles)

    def show_tournament_in_progress(self, tournament_key):
        """ Main method, resume and manages the tournament, creates rounds and launches menus """

        while True:
            # here to refresh the object
            my_tournament = DTournament().get_object_by_key(tournament_key)
            self.titles.update_subtitle(f"Tournoi : {my_tournament.name}", SubtitleLevel.FIRST)

            # First round
            if not my_tournament.round_keys:
                self._new_round(my_tournament)
            else:
                last_round = DRound().get_object_by_key(my_tournament.round_keys[-1])

                # Last round finished
                if last_round.datetime_end is not None:

                    if len(my_tournament.round_keys) < my_tournament.number_of_rounds:
                        self._new_round(my_tournament, my_tournament.round_keys)
                    else:
                        # Tournament finished
                        # Show a text to make a transition
                        self.view_menu.print_titles()
                        self.view_menu.print_text(f"Tounoi ** {my_tournament.name} ** terminé !")

                        # Save and show abstract
                        my_tournament.ended = True
                        DTournament().update_object(my_tournament)
                        self.controller_tournament.abstract_tournament(my_tournament)
                        return None

            # Launch menu with last round
            if self.menu_round.show_menu_round(my_tournament.round_keys[-1],
                                               my_tournament.key) == "Quit":
                return None

    def _new_round(self, tournament, previous_rounds_keys=[]):
        """ Private, create a new round with the controller round and
            save in the database """

        new_round = self.controller_round.create_round(tournament.players,
                                                       previous_rounds_keys)

        tournament.round_keys.append(new_round.key)
        DTournament().update_object(tournament)

        # Show a text to make a transition
        self.titles.clear_subtitle(SubtitleLevel.SECOND)
        self.titles.clear_subtitle(SubtitleLevel.THIRD)
        self.view_menu.print_titles()
        self.view_menu.print_line_break()
        self.view_menu.print_text(f"Création du round : ** {new_round.name} **", center=True)

    def show_new_tournament(self):
        """ Show menu to create a new tournament then launches the
            tournament in progress method """

        # Enough players (eight today 21/12/2021) ?
        if len(DPlayer().get_all_objects()) <= 8:
            self.titles.update_subtitle("Création d'un tournoi", SubtitleLevel.FIRST)
            self.view_menu.print_titles()
            self.view_menu.print_line_break()
            self.view_menu.print_text("Le nombre de joueurs est insuffisant pour "
                                      "pouvoir créer un nouveau tournoi.")
            return None

        else:
            # Create tournament and select 8 players
            self.titles.update_subtitle("Création d'un tournoi", SubtitleLevel.FIRST)
            my_tournament = self.controller_tournament.create_tournament()

            self.titles.update_subtitle(f"Création du tournoi : {my_tournament.name}",
                                        SubtitleLevel.FIRST)
            self.titles.update_subtitle(f"Selectionner {my_tournament.number_of_players} joureurs",
                                        SubtitleLevel.SECOND)
            player_keys = self.controller_player.selection_player(my_tournament.number_of_players)

            # Save player keys and init their points {'player_key':points}
            for p in player_keys:
                my_tournament.players[p] = 0

            DTournament().update_object(my_tournament)

            # Launch the progress menu with the new tournament
            self.show_tournament_in_progress(my_tournament.key)

    def show_resume_tournament(self):
        """ Search active tournaments and allow to select one.
            After the user choice, launches the tournament in progress method """
        tournaments = DTournament().get_all_objects()

        # Search active tournaments
        tournaments_active = []
        for t in tournaments:
            if not t.ended:
                tournaments_active.append(t)

        if not tournaments_active:
            self.view_menu.print_titles()
            self.view_menu.print_line_break()
            self.view_menu.print_text("Aucun tournoi en cours.")
        else:
            self.titles.update_subtitle("Selectionner le tournoi à reprendre",
                                        SubtitleLevel.SECOND)
            self.view_menu.print_titles()

            # Sort by date and ask selection
            tournaments_active.sort(key=attrgetter("date"), reverse=True)
            selected_tournament = self.controller_tournament.selection_tournament(
                tournaments_active)

            # Launch the progress menu
            self.show_tournament_in_progress(selected_tournament.key)
