#! env/bin/python3

from tinydb import TinyDB, Query
from random import randint

from controlbase import ControllerBase
from model.modelplayer import Player
from view.viewform import FormatData

class ControllerPlayer(ControllerBase):

    def __init__(self):
        super().__init__("players.json")

    def create_player(self):
        """ Create and show a form. User fill it and a new player is created in the data base """
        self.view_form.update_subtitle("Creation d'un joueur")

        my_demands = {"name" : {"name" : "Prénom", "format" : FormatData.STR},
                      "last_name" : {"name" : "Nom", "format" : FormatData.STR},
                      "birthday" : {"name" : "Date de naissance", "format" : FormatData.DATE},
                      "sex" : {"name" : "Sexe", "format" : FormatData.LIST, "choices" : ("Masculin", "Féminin")}}

        while True:
            # Ask each demands by ViewForm then create a player with user's values
            my_demands = self.view_form.show_form(my_demands)
            new_player = Player(super()._generate_key(), my_demands['name']['value'], my_demands['last_name']['value'], my_demands['birthday']['value'], my_demands['sex']['value'])

            if new_player.serialize() in self.data_base.all():
                self.view_form.print_titles()
                self.view_form.print_text(f"Le joueur {new_player.name} {new_player.last_name} exite déjà")
            else:
                self.data_base.insert(new_player.serialize())
                self.view_form.print_titles()
                self.view_form.print_text(f"Nouveau joueur ajouté :\n{new_player}")
                break

    def selection_player(self, number=1):
        """ Show all players in database and allow to select one or several.
            Return a list with the database key(s) of user(s) selected """
        if number == 1:
            self.view_menu.update_subtitle(f"Selection de un joueur")
        else:
            self.view_menu.update_subtitle(f"Selection de {number} joueurs")

        players = super().elements_sorted(("last_name", "name"))

        # Demands for the form
        my_demands = dict()
        for i, p in enumerate(players):
            my_demands[i] = f"{p['name']} - {p['last_name']} - rank : {p['rank']}"

        # Form filled by user (return user's choices)
        players_selected = self.view_menu.show_menu(my_demands, number)

        # Convert dictionary keys by TinyDB keys
        players_selected_id = []
        for i in players_selected:
            print(my_demands[i])
            players_selected_id.append(players[i]['key'])

        return players_selected_id

    def list_players(self, sorted_by=["last_name", "name", "rank"]):
        """ Show all players sorted with the keys in 'sorted_by' """
        self.view_form.update_subtitle("Liste des joueurs")
        players = super().elements_sorted(sorted_by)

        text = str()
        for p in players:
            text += f" - {p['name']} - {p['last_name']} - {p['birth']} - {p['sex']} - rank : {p['rank']}\n"

        self.view_form.print_titles()
        self.view_form.print_text(text)


if __name__ == "__main__":
    my_controler = ControllerPlayer()
    my_controler.selection_player(3)
    my_controler.list_players()
    #my_controler.create_player()

