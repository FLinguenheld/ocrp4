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
                        self.view_menu.print_line_break()
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
        self.titles.clear_subtitle(SubtitleLevel.FOURTH)
        self.view_menu.print_titles()
        self.view_menu.print_line_break()
        self.view_menu.print_text(f"Création du round : ** {new_round.name} **", center=True)

    def show_new_tournament(self):
        """ Shows menu to create a new tournament then launches the
            tournament in progress method """

        # Enough players
        if not DPlayer().get_all_objects():
            self.titles.update_subtitle("Création d'un tournoi", SubtitleLevel.FIRST)
            self.view_menu.print_titles()
            self.view_menu.print_line_break()
            self.view_menu.print_text("La base de données ne contient aucun joueur.")
            return None

        else:
            # Create tournament
            self.titles.update_subtitle("Création d'un tournoi", SubtitleLevel.FIRST)
            my_tournament = self.controller_tournament.create_tournament()

            # Adds players, if ok, launches the progress menu tournament
            if self._add_players(my_tournament):
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

            # Checks if players were selected, if not launches _add_players()
            if not selected_tournament.players:
                if not self._add_players(selected_tournament):
                    return None

            # Launch the progress menu
            self.show_tournament_in_progress(selected_tournament.key)

    def _add_players(self, tournament):
        """ Checks the number of players in the database and asks to user to select
            the number of players saved in the tournament model
            Then, saved the modification.
            Return True if adding is ok """

        self.titles.update_subtitle(f"Création du tournoi : {tournament.name}",
                                    SubtitleLevel.FIRST)

        # Checks if there are enough players
        if len(DPlayer().get_all_objects()) < tournament.number_of_players:
            self.view_menu.print_titles()
            self.view_menu.print_line_break()
            self.view_menu.print_text(f"La base de données ne contient pas assez de joueurs :\n"
                                      f"{tournament.number_of_players} joueurs nécessaires pour "
                                      f"{len(DPlayer().get_all_objects())} joueurs disponibles")
            return False

        else:
            self.titles.update_subtitle(f"Selectionner {tournament.number_of_players} joureurs",
                                        SubtitleLevel.SECOND)
            # Ask to user
            while True:
                player_keys = self.controller_player.selection_player(tournament.number_of_players)

                # Create a text to ask a confirmation
                txt = "\n"
                for k in player_keys:
                    txt += DPlayer().get_object_by_key(k).complete_name + "\n"

                self.titles.update_subtitle("Valider les joureurs", SubtitleLevel.SECOND)
                if self.view_menu.ask_confirmation(txt):
                    break

            # Saves players keys and init their points {'player_key':points}
            for p in player_keys:
                tournament.players[p] = 0

            DTournament().update_object(tournament)
            return True
