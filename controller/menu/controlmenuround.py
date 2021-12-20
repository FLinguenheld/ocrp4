#! env/bin/python3
""" Menu controller for rounds """
from os import getcwd
from sys import path
path.insert(1, getcwd())

from controller.menu.controlmenubase import ControllerMenuBase
from controller.controlround import ControllerRound
from controller.controlmatch import ControllerMatch
from view.viewbase import SubtitleLevel

from database.dataround import DRound
from database.datamatch import DMatch
from database.dataplayer import DPlayer
from database.datatournament import DTournament


class ControllerMenuRound(ControllerMenuBase):
    """ Regroup menus to manage the rounds """

    def __init__(self, titles, round_key, tournament_key):
        super().__init__(titles)
        self.controller_round = ControllerRound(titles)
        self.round = DRound().get_object_by_key(round_key)
        self.tournament = DTournament().get_object_by_key(tournament_key)

    def show_menu_round(self):
        """ Show the menu of a round, allow to indicate score, validate round, and
            show the classement. 
            Subtitles are used to show the current matches results """    

        while True:

            self.titles.update_subtitle(f"{self.round.name} - {self.round.datetime_start}",
                                        SubtitleLevel.SECOND)
            self.titles.update_subtitle(self.controller_round.abstract_round(self.round),
                                        SubtitleLevel.THIRD)
            self.titles.clear_subtitle(SubtitleLevel.FOURTH)

            my_demands = {1:"Renseigner score",
                          2:"Valider round",
                         'a':None,
                          3:"Afficher le classement en cours",
                         'b':None,
                          4:"Quitter"}

            choice = self.view_menu.show_menu(my_demands)

            if choice == 1:
                self._show_menu_scores()

            elif choice == 2:
                self._validate_round()
                return None

            elif choice == 3:
                self.titles.update_subtitle("Classement en cours", SubtitleLevel.FOURTH)
                self.view_menu.print_titles()
                self.view_menu.print_line_break()
                self.view_menu.print_text(
                        self.controller_tournament.tournament_ranking(self.tournament))

            else:
                return None


    def _validate_round(self):
        """ Allow to validate round if matches are finished.
            Update the round and the tournament and save in databases """

        matches = DMatch().get_objects_by_keys(self.round.match_keys)

        # Check if all matches are complete
        for m in matches:
            if m.winner == None:

                self.titles.update_subtitle(f"Validation du round", SubtitleLevel.FOURTH)
                self.view_menu.print_titles()
                self.view_menu.print_line_break()
                self.view_menu.print_text("Tous les matchs doivent être terminés "\
                                          "pour pouvoir valider le round.")
                return None

        # If ok, add points in tournament
        for m in DMatch().get_objects_by_keys(self.round.match_keys):

            if m.winner == 0:
                self.tournament.players[m.player_keys[0]] += 0.5
                self.tournament.players[m.player_keys[1]] += 0.5
            else:
                self.tournament.players[m.winner] += 1

        DTournament().update_object(self.tournament)
        
        # Save the date of end
        self.round.save_datetime_end()
        DRound().update_object(self.round)


    def _show_menu_scores(self):
        """ Show matches and allow to select one to complete the winner """
        while True:
            self.titles.update_subtitle(self.controller_round.abstract_round(self.round),
                                        SubtitleLevel.THIRD)
            self.titles.update_subtitle("Sélectionner un match pour modifier le résultat",
                                        SubtitleLevel.FOURTH)

            matches = DMatch().get_objects_by_keys(self.round.match_keys)
            my_demands = {}
            for i, m in enumerate(matches):
                my_demands[i] = f"{DPlayer().get_object_by_key(m.player_keys[0]).complete_name} - "\
                                f"{DPlayer().get_object_by_key(m.player_keys[1]).complete_name}"

            my_demands['a'] = None
            my_demands[len(my_demands) - 1] = "Quitter"
            choice = self.view_menu.show_menu(my_demands)

            if choice < len(matches):
                self.titles.update_subtitle("Sélectionner le vainqueur",
                                            SubtitleLevel.FOURTH)

                my_controller_match = ControllerMatch(self.titles)
                my_controller_match.set_winner(matches[choice])
            else:
                return None

