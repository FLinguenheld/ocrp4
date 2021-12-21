#! env/bin/python3
""" Controller for players """
from os import getcwd
from sys import path
path.insert(1, getcwd())

from operator import attrgetter

from controller.controlbase import ControllerBase
from view.viewform import FormatData

from model.modelplayer import MPlayer
from database.dataplayer import DPlayer


class ControllerPlayer(ControllerBase):
    """ Regroup main methods to manage model and database players """

    def __init__(self, titles):
        super().__init__(titles)

    def create_player(self):
        """ Create a player in database.
            Show a form and check if new player already exists. 
            Then save in database and return the new player """

        new_player = self._form_player()
        DPlayer().add_object(new_player)

        self.view_form.print_line_break()
        self.view_form.print_text(f"Nouveau joueur ajouté :\n" \
                                  f"  ** {new_player}")
        return new_player

    def update_player(self, player):
        """ Update a player in the database.
            Show a form and test if the updated player player exists.
            Then update the database and return the updated player.
            Attr 'player' is used to pre-fill the form """

        updated_player = self._form_player(player)
        DPlayer().update_object(updated_player)

        self.view_form.print_line_break()
        self.view_form.print_text(f"Le joueur :\n  ** {player}", ask_to_continue=False)
        self.view_form.print_line_break()
        self.view_form.print_text(f"a été remplacé par :\n  ** {updated_player}")
        return updated_player

    def _form_player(self, player=None):
        """ Create a form and ask to user to fill it.
            Check if new player already exists.
            Give a player to pre-fill the form.
            Return new player created """

        while True:
            # Empty player if needed
            if player is None:
                player = MPlayer()

            my_demands = {"name" :
                                {"name" : "Prénom",
                                 "format" : FormatData.STR,
                                 "value" : player.name},
                          "last_name" :
                                {"name" : "Nom",
                                 "format" : FormatData.STR,
                                 "value" : player.last_name},
                          "birth" :
                                {"name" : "Date de naissance",
                                 "format" : FormatData.DATE,
                                 "value" : player.birth},
                          "sex" :
                                {"name" : "Sexe",
                                 "format" : FormatData.LIST,
                                 "choices" : ("Masculin", "Féminin"),
                                 "value" : player.sex}}

           # Show form and create a player with new values
            my_demands = self.view_form.show_form(my_demands)
            new_player = MPlayer(   player.key,
                                    my_demands['name']['value'],
                                    my_demands['last_name']['value'],
                                    my_demands['birth']['value'],
                                    my_demands['sex']['value'],
                                    player.rank)

            self.view_form.print_titles(clear_before=True)
            if new_player in DPlayer().get_all_objects():
                self.view_form.print_text(
                                    f"Le joueur {new_player.complete_name} exite déjà")
            else:
                return new_player

    def selection_player(self, number=1):
        """ Show all players in database and allow to select one or several.
            Return a list with the database key(s) of user(s) selected.
            Or just a key (int) if number=1 """

        players = DPlayer().get_all_objects()
        players.sort(key=attrgetter("rank"), reverse=True)
        players.sort(key=lambda k:k.name.lower(), reverse=False)
        players.sort(key=lambda k:k.last_name.lower(), reverse=False)

        # Demands for the form
        my_demands = dict()
        for i, p in enumerate(players):
            my_demands[i] = f"{p}"

        # Form filled by user (return user's choices in a list)
        players_selected_in_form = self.view_menu.show_menu(my_demands, number)

        if isinstance(players_selected_in_form, int):
            return players[players_selected_in_form].key
        else:
            # Convert the list user's choices keys by TinyDB keys
            players_selected_keys_in_db = []
            for i in players_selected_in_form:
                players_selected_keys_in_db.append(players[i].key)

            return players_selected_keys_in_db
    
