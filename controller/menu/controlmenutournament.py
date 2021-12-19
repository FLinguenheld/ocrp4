#! env/bin/python3
from os import getcwd
from sys import path
path.insert(1, getcwd())


from controller.menu.controlmenubase import ControllerMenuBase
from controller.menu.controlmenuround import ControllerMenuRound

from controller.controltournament import ControllerTournament
from controller.controlplayer import ControllerPlayer
from controller.controlround import ControllerRound

from model.modeltournament import MTournament
from model.modelplayer import MPlayer
from database.dataplayer import DPlayer
from view.viewbase import SubtitleLevel

from database.datatournament import DTournament
from database.dataround import DRound

class ControllerMenuTournament(ControllerMenuBase):

    def __init__(self, titles):
        super().__init__(titles)
        self.controller_tournament = ControllerTournament(self.titles)
        self.controller_player = ControllerPlayer(self.titles)
        self.controller_round = ControllerRound(self.titles)

    def show_tournament_in_progress(self, tournament_key):

        my_tournament = DTournament().get_object_by_key(tournament_key)
        self.titles.update_subtitle(f"Tournoi : {my_tournament.name}", SubtitleLevel.FIRST)

        while True:

            # First round
            if not my_tournament.round_keys:
                self._new_round(my_tournament)
            else:
                last_round = DRound().get_object_by_key(my_tournament.round_keys[-1])

                # Last round finished
                if last_round.datetime_end != None:

                    if len(my_tournament.round_keys) < my_tournament.number_of_rounds:
                        self._new_round(my_tournament, my_tournament.round_keys)
                    else:
                        # Tournament finished
                        my_tournament.ended = True
                        DTournament.update_object(my_tournament)
                        self.controller_tournament.abstract_tournament(my_tournament)
                        return None

            # Launch menu with last round
            menu_round = ControllerMenuRound(self.titles, my_tournament.round_keys[-1], my_tournament.key)
            menu_round.show_menu_round()

    def _new_round(self, tournament, previous_rounds_keys=[]):
        new_round = self.controller_round.create_round(tournament.players, previous_rounds_keys)

        tournament.round_keys.append(new_round.key)
        DTournament().update_object(tournament)



    def show_new_tournament(self):

        # Enough players ?
        if len(self.database_player.get_all_objects([])) <= 8:
            self.titles.update_subtitle("Création d'un tournoi", SubtitleLevel.FIRST)
            self.view_menu.print_titles()
            self.view_menu.print_text("Le nombre de joueurs est insuffisant pour "\
                                       "pouvoir créer un nouveau tournoi.")

            return 0
        else:
            # Create tournament and select 8 players
            self.titles.update_subtitle("Création d'un tournoi", SubtitleLevel.FIRST)
            my_tournament = self.controller_tournament.create_tournament()            

            self.titles.update_subtitle(f"Création du tournoi : {my_tournament.name}",
                                        SubtitleLevel.FIRST)
            self.titles.update_subtitle("Selectionner 8 joureurs", SubtitleLevel.SECOND)
            player_keys = self.controller_player.selection_player(8)

            # Save player keys and init their points {'olayer_key':points}
            for p in player_keys:
                my_tournament.players[p] = 0

            DTournament().update_object(my_tournament)

            # Launch the progress menu
            self.show_tournament_in_progress(my_tournament.key)


    def show_resume_tournament(self):
        tournaments = DTournament().get_all_objects([])

        # Search active tournaments
        tournaments_active = []
        for t in tournaments:
            if t.ended == False:
                tournaments_active.append(t)

        if not tournaments_active:
            self.view_menu.print_titles()
            self.view_menu.print_text("Aucun tournoi en cours.")
        else:
            self.titles.update_subtitle("Selectionner le tournoi à reprendre",
                                        SubtitleLevel.SECOND)
            self.view_menu.print_titles()

            selected_tournament = self.controller_tournament.selection_tournament(
                                    tournaments_active)
            
            # Launch the progress menu
            self.show_tournament_in_progress(selected_tournament.key)


if __name__ == "__main__":
    my_menu = ControllerMenuTournament()
    my_menu.show_new_tournament()
