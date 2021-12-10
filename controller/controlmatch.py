#! env/bin/python3
from os import getcwd
from sys import path
path.insert(1, getcwd())

from controller.controlbase import ControllerBase
from model.modelmatch import MMatch
from model.modelplayer import MPlayer
from database.datamatch import DMatch

class ControllerMatch(ControllerBase):

    def __init__(self):
        super().__init__()

    def set_winner(self, match_key):
        """ Show a form to choice the winner
            After user's choice, update the databases (database matchs and players) """

        my_match = self.database_match.get_object_by_key(match_key)
        player1 = self.database_player.get_object_by_key(my_match.player_keys[0])
        player2 = self.database_player.get_object_by_key(my_match.player_keys[1])

        while True:
            # Form
            self.view_menu.update_subtitle(f"Selection du vainqueur")
            my_demands = {1:f"{player1}", 2:f"{player2}", 'a':None, 3:"Égalité"}
            winner_index = self.view_menu.show_menu(my_demands)

            # Affect the winner
            if winner_index == 1:
                winner = player1
            elif winner_index == 2:
                winner = player2
            else:
                winner = None

            # Text for confirmation
            if winner is not None:
                txt_confirmation = f"Vainqueur : {winner}"
            else:
                txt_confirmation = "Égalité"

            # Ask a confirmation and update databases
            if self.view_menu.ask_confirmation(txt_confirmation):

                if winner is not None:
                    my_match.winner = winner.key
                    self._maj_rank(winner, 1)
                else:
                    my_match.winner = 0 
                    self._maj_rank(player1, 0.5)
                    self._maj_rank(player2, 0.5)

                # Update database macth and leave
                self.database_match.update_object(my_match)
                break

    def _maj_rank(self, player, value):
        """ Add value to the player's points and update in database player """
        player.points += value
        self.database_player.update_object(player)

        
if __name__ == "__main__":
    my_controller = ControllerMatch()

    my_match = MMatch(42861001, [66601745, 30498973])
    database_match = DMatch()  
    database_match.add_object(my_match)
    print(my_match)

    my_controller.set_winner(my_match.key)

