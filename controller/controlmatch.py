#! env/bin/python3
from os import getcwd
from sys import path
path.insert(1, getcwd())

from controller.controlbase import ControllerBase
from model.modelmatch import MMatch
from model.modelplayer import MPlayer
from database.datamatch import DMatch
from view.viewbase import Title

class ControllerMatch(ControllerBase):

    def __init__(self, titles):
        super().__init__(titles)

    def set_winner(self, match):
        """ Show a form to choice the winner
            After user's choice, update the database
            Return a dict with the player's key and the points to add """

        player1 = self.database_player.get_object_by_key(match.player_keys[0])
        player2 = self.database_player.get_object_by_key(match.player_keys[1])

        # Form
        my_demands = {1:f"{player1}", 2:f"{player2}",
                     'a':None,
                      3:"Égalité",
                     'b':None,
                      4:"En cours"}

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
        self.database_match.update_object(match)

        
if __name__ == "__main__":

    my_titles = Title("Titre d'essai - control match")
    my_titles.update_subtitle("Sous titre") 

    my_controller = ControllerMatch(my_titles)

    my_match = MMatch(42861001, [81059600, 27054088])
    database_match = DMatch()  
    database_match.add_object(my_match)

    my_controller.set_winner(my_match)

