#! env/bin/python3
from os import getcwd
from sys import path
path.insert(1, getcwd())


from controller.menu.controlmenubase import ControllerMenuBase
from controller.controlround import ControllerRound
from view.viewbase import SubtitleLevel

from controller.controlmatch import ControllerMatch


from database.datamatch import DMatch


class ControllerMenuRound(ControllerMenuBase):

    def __init__(self, titles, round_key, tournament_key):
        super().__init__(titles)
        self.controller_round = ControllerRound(titles)
        self.round = self.database_round.get_object_by_key(round_key)
        self.tournament = self.database_tournament.get_object_by_key(tournament_key)


    def show_menu_round(self):
    

        while True:

            self.titles.update_subtitle(f"{self.round.name} - {self.round.datetime_start}",
                                        SubtitleLevel.SECOND)
            self.titles.update_subtitle(self._build_synopsis(),
                                        SubtitleLevel.THIRD)
            self.titles.clear_subtitle(SubtitleLevel.FOURTH)

            my_demands = {1:"Renseigner score",
                          2:"Valider round",
                         'a':None,
                          3:"Afficher la liste des joueurs",
                         'b':None,
                          4:"Quitter"}

            choice = self.view_menu.show_menu(my_demands)

            if choice == 1:
                self._show_menu_scores()

            elif choice == 2:
                pass


            elif choice == 3:
                self._show_players()


            else:
                return None

    def _show_players(self):
        
        # Players list (already sort by model)
        text = str()
        for i, (key, points) in enumerate(self.tournament.players.items()):
            if points > 1:
                text += f"{i + 1} − {self._get_player_name(key)} - {points} points\n"
            else:
                text += f"{i + 1} − {self._get_player_name(key)} - {points} point\n"


        self.titles.update_subtitle("Classement en cours", SubtitleLevel.FOURTH)
        self.view_menu.print_titles()
        self.view_menu.print_text(text)


    def _show_menu_scores(self):
        """ Show matches and allow to select one to complete the winner """
        while True:
            self._build_synopsis()
            self.titles.update_subtitle(self._build_synopsis(),
                                        SubtitleLevel.THIRD)
            self.titles.update_subtitle("Sélectionner un match pour indiquer le résultat",
                                        SubtitleLevel.FOURTH)

            matches = self.database_match.get_objects_by_keys(self.round.match_keys)
            my_demands = {}
            for i, m in enumerate(matches):
                my_demands[i] = f"{self._get_player_name(m.player_keys[0])} - "\
                                f"{self._get_player_name(m.player_keys[1])}"

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


    def _build_synopsis(self):
        """ Refresh synopsis to show matchs list and winners
            Return a text """
        # Have to use a new DMatch because without, TinyDB return old datas
        my_matches = DMatch().get_objects_by_keys(self.round.match_keys)

        synopsis = "\n"
        for m in my_matches:
            synopsis += self._get_player_name(m.player_keys[0])
            synopsis += " - "
            synopsis += self._get_player_name(m.player_keys[1])

            if m.winner is None:
                synopsis += " - En cours\n"
            elif m.winner == 0:
                synopsis += " - Égalité\n"
            else:
                synopsis += f" - vainqueur : {self._get_player_name(m.winner)}\n"

        return synopsis

    def _get_player_name(self, player_key):
        """ Return the player's name with a key """
        player = self.database_player.get_object_by_key(player_key)
        return f"{player.name} {player.last_name}"



    def show_list_matchs(self):
        pass


    def show_select_winner(self):
        pass
