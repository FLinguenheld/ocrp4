#! env/bin/python3
""" Controller for tournament """
from os import getcwd
from sys import path
path.insert(1, getcwd())

from controller.controlbase import ControllerBase
from controller.controlround import ControllerRound

from view.viewform import FormatData
from view.viewbase import SubtitleLevel

from model.modeltournament import MTournament
from database.datatournament import DTournament
from database.dataplayer import DPlayer
from database.dataround import DRound


class ControllerTournament(ControllerBase):
    """ Regroup main methods to manage model and database tournaments """

    def __init__(self, titles):
        super().__init__(titles)
        self.controller_round = ControllerRound(titles)

    def abstract_tournament(self, tournament):
        """ Build a text with the current results of the tournament
            saved in the database """

        self.titles.clear_subtitle(SubtitleLevel.ALL)
        self.titles.update_subtitle(f"Tournoi : {tournament.name}", SubtitleLevel.FIRST)

        # --
        if not tournament.ended:
            self.titles.update_subtitle("EN COURS", SubtitleLevel.SECOND)
        else:
            self.titles.update_subtitle("TERMINÉ", SubtitleLevel.SECOND)

        # -−
        text = f"Du {tournament.date_start} au {tournament.date_end}\n"
        text += f"Ville : {tournament.place}\n"
        text += f"Nombre de joueurs : {tournament.number_of_players}"
        text += f"Nombre de rounds : {tournament.number_of_rounds}\n"
        text += f"Contrôle du temps : {tournament.time_control}\n"
        text += f"Description : {tournament.description}"
        self.titles.update_subtitle(text, SubtitleLevel.THIRD)
        self.view_menu.print_titles()

        # Players
        self.view_menu.print_text("** Participants **\n", ask_to_continue=False)
        self.view_menu.print_text(self.players_list(tournament))
        self.view_menu.print_separator()

        # Ranking
        self.view_menu.print_text("** Classement **\n", ask_to_continue=False)
        self.view_menu.print_text(self.tournament_ranking(tournament))
        self.view_menu.print_separator()

        # --
        if tournament.round_keys:

            for round_key in tournament.round_keys:

                my_round = DRound().get_object_by_key(round_key)
                text = str()
                text += f"** {my_round.name} **\n"
                if my_round.datetime_end is not None:
                    text += f"** Du {my_round.datetime_start} au {my_round.datetime_end} **"
                else:
                    text += f"** Du {my_round.datetime_start} au (round en cours) **"

                self.view_menu.print_text(text, ask_to_continue=False)
                self.view_menu.print_text(self.controller_round.abstract_round(my_round))
                self.view_menu.print_separator()

    def players_list(self, tournament):
        """ Return a text with the name of players in the tournament """
        players = []
        for k in tournament.players.keys():
            players.append(DPlayer().get_object_by_key(k))

        players.sort(key=lambda k: k.last_name.lower(), reverse=False)
        players.sort(key=lambda k: k.name.lower(), reverse=False)

        txt = str()
        for p in players:
            txt += f"{p.complete_name} - ({p.rank})\n"

        return txt

    def tournament_ranking(self, tournament):
        """ Return a text with the current ranking.
            Players list is already sort by model """

        text = str()
        i = 1
        previous_points = -1
        for key, points in tournament.players.items():
            player = DPlayer().get_object_by_key(key)
            if points != previous_points:
                if points > 1:
                    text += f"{i} − {player.complete_name} - {points} points\n"
                else:
                    text += f"{i} − {player.complete_name} - {points} point\n"
                i += 1
                previous_points = points
            else:
                text += f"    {player.complete_name}\n"

        return text[:-1]

    def create_tournament(self):
        """ Create and show a form. User fill it and a new tournament is created in the data base
            Return the instance of the new object created """

        my_demands = {"name":
                      {"name": "Nom du tournoi", "format": FormatData.STR},
                      "place":
                      {"name": "Ville", "format": FormatData.STR},
                      "date_start":
                      {"name": "Date de début", "format": FormatData.DATE},
                      "date_end":
                      {"name": "Date de fin", "format": FormatData.DATE},
                      "number_of_players":
                      {"name": "Nombre de joueurs", "format": FormatData.LISTINT, "choices": [8, 10]},
                      "number_of_rounds":
                      {"name": "Nombre de rounds", "format": FormatData.LISTINT, "choices": [4, 6]},
                      "time_control":
                      {"name": "Contrôle du temps", "format": FormatData.LIST,
                          "choices": ("Bullet", "Blitz", "Coup rapide")},
                      "description":
                      {"name": "Description", "format": FormatData.STR}}

        while True:
            # Ask each demands by ViewForm then create a tournament with user's values
            my_demands = self.view_form.show_form(my_demands)
            new_tournament = MTournament(0,
                                         my_demands['name']['value'],
                                         my_demands['place']['value'],
                                         my_demands['date_start']['value'],
                                         my_demands['date_end']['value'],
                                         my_demands['number_of_players']['value'],
                                         my_demands['number_of_rounds']['value'],
                                         my_demands['time_control']['value'],
                                         my_demands['description']['value'])

            self.view_form.print_titles(True)
            if new_tournament in DTournament().get_all_objects():
                self.view_form.print_text(f"Le tournoi {new_tournament.name} de "
                                          f"{new_tournament.place} exite déjà")
            else:
                DTournament().add_object(new_tournament)
                self.view_form.print_line_break()
                self.view_form.print_text(f"Nouveau tournoi ajouté :\n{new_tournament}")
                return new_tournament

    def selection_tournament(self, tournaments_list):
        """ Show the tournaments list and allow to select one or several.
            Return an object of the selected tournament """

        # Demands for the form
        my_demands = dict()
        for i, p in enumerate(tournaments_list):
            my_demands[i] = f"{p}"

        # Form filled by user (return user's choices in a list)
        tournament_selected_in_form = self.view_menu.show_menu(my_demands, number_of_choices=1)
        return tournaments_list[tournament_selected_in_form]
