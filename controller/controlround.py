#! env/bin/python3
""" Controller for rounds """
from os import getcwd
from sys import path
path.insert(1, getcwd())

from controller.controlbase import ControllerBase

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

        # Get previous matches played in all previous rounds
        previous_matches = self._get_all_previous_matches(previous_rounds_keys)

        # Get MPlayers and sort players by points
        my_players = self._sort_players(players_key_points)
        matchs_keys = []

        while my_players:

            # Cut in two lists
            middle_index = len(my_players) // 2
            first_list = my_players[:middle_index]
            second_list = my_players[middle_index:]
            second_list += first_list

            # p1 with p2 exept is match already play with this two players
            p1 = first_list[0]
            for p2 in second_list:

                if p1.key != p2.key:
                    new_match = MMatch(0, [p1.key, p2.key])

                    # Already played ?
                    if new_match not in previous_matches:

                        # Create the match, save in database and add in the list
                        new_match_key = DMatch().add_object(new_match)
                        matchs_keys.append(new_match_key)

                        # Remove players from list
                        my_players.remove(p2)
                        my_players.remove(p1)
                        break

        # Create round, save in database and return the object
        name = "Round " + str(len(previous_rounds_keys) + 1)
        new_round = MRound(0, name, matchs_keys)
        new_round.save_datetime_start()
        DRound().add_object(new_round)
        return new_round

    def _get_all_previous_matches(self, previous_rounds_keys):
        """ Return a list with all previous matches played during all previous
            rounds """
        # Loop if rounds
        previous_matches_keys = []
        for round_key in previous_rounds_keys:
            my_round = DRound().get_object_by_key(round_key)
            previous_matches_keys += my_round.match_keys

        # Loop in matches
        previous_matches = []
        for match_key in previous_matches_keys:
            previous_matches.append(DMatch().get_object_by_key(match_key))

        return previous_matches

    def _sort_players(self, players):
        """ Get the MPlayers objects, save their points,
            build a list and sort by rank then by points """

        my_players_list = []
        for key, points in players.items():
            my_player = DPlayer().get_object_by_key(int(key))
            my_player.points = points

            my_players_list.append(my_player)

        my_players_list.sort(key=lambda p: p.rank, reverse=True)
        my_players_list.sort(key=lambda p: p.points, reverse=True)

        return my_players_list
