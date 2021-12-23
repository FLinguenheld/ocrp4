#! env/bin/python3
""" Controller for matches """
from os import getcwd
from sys import path
path.insert(1, getcwd())

from controller.controlbase import ControllerBase

from database.datamatch import DMatch
from database.dataplayer import DPlayer


class ControllerMatch(ControllerBase):
    """ Regroup main methods to manage model and database matches """

    def __init__(self, titles):
        super().__init__(titles)

    def set_winner(self, match):
        """ Show a form to choice the winner
            After user's choice, update the database
            Return a dict with the player's key and the points to add """

        player1 = DPlayer().get_object_by_key(match.player_keys[0])
        player2 = DPlayer().get_object_by_key(match.player_keys[1])

        # Form
        my_demands = {1: f"{player1}",
                      2: f"{player2}",
                      'a': None,
                      3: "Égalité",
                      'b': None,
                      4: "En cours"}

        winner_index = self.view_menu.show_menu(my_demands)

        # Affect the winner
        if winner_index == 1:
            match.winner = player1.key

        elif winner_index == 2:
            match.winner = player2.key

        elif winner_index == 3:
            match.winner = 0

        else:
            match.winner = None

        # Update database macth
        DMatch().update_object(match)
