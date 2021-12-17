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


class ControllerMenuTournament(ControllerMenuBase):

    def __init__(self, titles):
        super().__init__(titles)
        self.controller_tournament = ControllerTournament(self.titles)
        self.controller_player = ControllerPlayer(self.titles)
        self.controller_round = ControllerRound(self.titles)

    def show_tournament_in_progress(self, tournament):

        self.titles.update_subtitle(f"Tournoi {tournament.name}", SubtitleLevel.FIRST)
        

        # Create the first round if needed
        if not tournament.round_keys:
            first_round = self.controller_round.create_round(tournament.players)

            tournament.round_keys.append(first_round.key)
            self.database_tournament.update_object(tournament)

        menu_round = ControllerMenuRound(self.titles, tournament.round_keys[-1], tournament.key)
        menu_round.show_menu_round()





    def show_new_tournament(self):
        self.view_menu.print_titles()

        # Enough players ?
        if len(self.database_player.get_all_objects([])) <= 8:
            self.titles.update_subtitle("Création d'un tournoi", SubtitleLevel.FIRST)
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

            self.database_tournament.update_object(my_tournament)

            # Launch the progress menu
            self.show_tournament_in_progress(my_tournament)


    def show_resume_tournament(self):
        tournaments = self.database_tournament.get_all_objects([])

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
            self.show_tournament_in_progress(selected_tournament)


if __name__ == "__main__":
    my_menu = ControllerMenuTournament()
    my_menu.show_new_tournament()
