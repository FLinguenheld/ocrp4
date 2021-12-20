#! env/bin/python3
""" Controller for rounds """
from os import getcwd
from sys import path
path.insert(1, getcwd())

from controller.controlbase import ControllerBase
from view.viewbase import Title

from model.modelround import MRound
from model.modelmatch import MMatch

from database.dataround import DRound
from database.datamatch import DMatch
from database.dataplayer import DPlayer


class ControllerRound(ControllerBase):
    """ Regroup main methods to manage model and database rounds """

    def __init__(self, titles):
        super().__init__(titles)

    def abstract_round(self, my_round):
        """ Build a text with the current results of
            the matches saved in the round """

        my_matches = DMatch().get_objects_by_keys(my_round.match_keys)

        abstract = "\n"
        for m in my_matches:
            abstract += DPlayer().get_object_by_key(m.player_keys[0]).complete_name
            abstract += " - "
            abstract += DPlayer().get_object_by_key(m.player_keys[1]).complete_name

            if m.winner is None:
                abstract += "  -  En cours\n"
            elif m.winner == 0:
                abstract += "  -  Égalité\n"
            else:
                abstract += f"  -  vainqueur : "\
                            f"{DPlayer().get_object_by_key(m.winner).complete_name}\n"
        return abstract

    def create_round(self, players_key_points={}, previous_rounds_keys=[]):
        """ Create and save a round in the database
            Manage the swiss system to create matches """

        name = "Round " + str(len(previous_rounds_keys) + 1)
        
        # Get MPlayers and sort players by points
        middle_index = len(players_key_points) // 2
        my_players = self._sort_players(players_key_points)

        # Cut in two lists
        first_list = my_players[:middle_index]
        second_list = my_players[middle_index:]

        # Matches creation
        match_keys = []
        for p1 in first_list:

            # p1 with p2 exept is match already play with this two players
            for p2 in second_list:
                new_match = MMatch(0, [p1.key, p2.key])
                print(new_match)

                # Already played ?
                if not self._check_match_already_played(new_match, previous_rounds_keys):

                    # Create the match, save in database and add in the list
                    new_match_key = DMatch().add_object(new_match)
                    match_keys.append(new_match_key)

                    second_list.remove(p2)
                    break

        # Create round, save in database and return the object
        new_round = MRound(0, name, match_keys)
        new_round.save_datetime_start()
        DRound().add_object(new_round)
        return new_round

    def _check_match_already_played(self, match, previous_rounds_keys):
        """ Get all matches in 'previous_rounds_keys' and check if a match
            with the sames players already exists """

        # get the previous matches 
        previous_matches = []
        for round_key in previous_rounds_keys:
            my_round = DRound().get_object_by_key(round_key)
            previous_matches += my_round.match_keys

        # Check if the match was already played
        for match_key in previous_matches:
            my_match = DMatch().get_object_by_key(match_key)
            if my_match == match:
                return True

        # Checking done
        return False

    def _sort_players(self, players):
        """ Get the MPlayers objects, save their points,
            build a list and sort by rank then by points """

        my_players_list = []
        for key, points in players.items():
            my_player = DPlayer().get_object_by_key(int(key))
            my_player.points = points

            my_players_list.append(my_player)

        my_players_list.sort(key=lambda p:p.rank, reverse=True)
        my_players_list.sort(key=lambda p:p.points, reverse=True)

        return my_players_list

  
if __name__ == "__main__":
    my_titles = Title("Titre d'essai")
    my_titles.update_subtitle("Sous titre d'essai aussi")
    my_controler = ControllerRound(my_titles)

    players = {"7953165": 0, "50891778": 0, "1553056": 0,
               "74882721": 0, "43745125": 0, "77652086": 0,
               "81059600": 0, "86303826": 0}


    my_controler.create_round(players)
