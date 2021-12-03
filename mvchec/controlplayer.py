#! env/bin/python3

from tinydb import TinyDB, Query

from view.viewform import VForm
from view.viewform import FormatData
from view.viewmenu import VMenu
from model.modelplayer import Player

class ControllerPlayer:

    def __init__(self):
        self.data_base = TinyDB("players.json")

        self.titles = ["GESTIONNAIRE DE TOURNOI D'ECHECS (à modifier)"]
        self.view_form = VForm(self.titles)
        self.view_menu = VMenu(self.titles)

    def create_player(self):
        self.view_form.update_subtitle("Creation d'un joueur")

        my_dem = {"name" : {"name" : "Prénom", "format" : FormatData.STR},
                  "last_name" : {"name" : "Nom", "format" : FormatData.STR},
                  "birthday" : {"name" : "Date de naissance", "format" : FormatData.DATE},
                  "sex" : {"name" : "Sexe", "format" : FormatData.LIST, "choices" : ("Masculin", "Féminin")}}

        while True:
            my_dem = self.view_form.show_form(my_dem)
            new_player = Player(my_dem['name']['value'], my_dem['last_name']['value'], my_dem['birthday']['value'], my_dem['sex']['value'])
#            new_player = Player("Gérald", "Trochu", "2021-01-01", "Masculin")
            
            if new_player.serialize() in self.data_base.all():
                self.view_form.print_titles()
                self.view_form.print_text(f"Le joueur {new_player.name} {new_player.last_name} exite déjà")
            else:
                self.data_base.insert(new_player.serialize())
                self.view_form.print_titles()
                self.view_form.print_text(f"Nouveau joueur ajouté :\n{new_player}")
                break
        
    def _sorted_players_list(self, by_rank=False):
        players = sorted(self.data_base.all(), key=lambda d:d['last_name'])
        players = sorted(self.data_base.all(), key=lambda d:d['name'])

        if by_rank:
            players = sorted(self.data_base.all(), key=lambda d:d['rank'])

        return players

    def selection_player(self, number=1, show_by_rank=False):
        self.view_menu.update_subtitle(f"Selection de {number} joueur(s)")

        players = self._sorted_players_list(show_by_rank)

        # Selection by user
        my_choices = dict()
        for i, p in enumerate(players):
            my_choices[i] = f"{p['name']} - {p['last_name']} - rank : {p['rank']}"

        players_selected = self.view_menu.show_menu(my_choices, number)



        # Convert dictionry keys by TinyDB keys
        players_selected_id = []
        for i in players_selected:
            players_selected_id.append(my_choices[i])



    def list_players(self, show_by_rank=False):
        self.view_form.update_subtitle("Liste des joueurs")



        text = str()
        players = self._sorted_players_list(show_by_rank)
        for p in players:
            text += f" - {p['name']} - {p['last_name']} - {p['birth']} - {p['sex']} - rank : {p['rank']}\n"

        self.view_form.print_titles()
        self.view_form.print_text(text)



        print(self.data_base.all()[0])

        print(self.data_base.get(doc_id=1))


    def test_db(self):

        #my_player = Player(my_dem['first_name']['value'], my_dem['last_name']['value'], my_dem['birthday']['value'], my_dem['sex']['value'])
        my_player = Player("Gérald", "Trochu", "2021-01-01", "Masculin")

        self.data_base.insert(my_player.serialize())

        print(self.data_base.all())

    def recup_db(self):


        db = TinyDB("test.json")

        
        my_player = Player()
        my_player.unserialize(db.all()[0])

        my_player2 = Player("uiestau")
        my_player2.last_name = "urnisetst"

        print(my_player == my_player2)

        print(my_player)


if __name__ == "__main__":



    my_controler = ControllerPlayer()

    #my_controler.selection_player(3)
    my_controler.list_players()

    #my_controler.create_player()

    #my_controler.test_db()

    #my_controler.recup_db()

