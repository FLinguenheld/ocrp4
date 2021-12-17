#! env/bin/python3
from os import getcwd
from sys import path
path.insert(1, getcwd())

from controller.controlbase import ControllerBase
from model.modeltournament import MTournament
from database.datatournament import DTournament


from view.viewform import FormatData
from view.viewbase import Title


class ControllerTournament(ControllerBase):

    def __init__(self, titles):
        super().__init__(titles)


    def resume_tournament(self, tournament):

        round_in_progress = self._find_round_not_finished(tournament)


        if round_in_progress == None:
            pass

            # Create a new round



        else:
            pass




    def create_tournament(self):
        """ Create and show a form. User fill it and a new tournament is created in the data base
            Return the instance of the new object created """

        my_demands = {"name" : {"name" : "Nom du tournoi", "format" : FormatData.STR},
                      "place" : {"name" : "Ville", "format" : FormatData.STR},
                      "date_start" : {"name" : "Date de début", "format" : FormatData.DATE},
                      "date_end" : {"name" : "Date de fin", "format" : FormatData.DATE},
                      "number_of_rounds" : {"name" : "Nombre de rounds", "format" : FormatData.LISTINT, "choices" : [4]},
                      "time_control" : {"name" : "Contrôle du temps", "format" : FormatData.LIST, "choices" : ("Bullet", "Blitz", "Coup rapide")},
                      "description" : {"name" : "Description", "format" : FormatData.STR}}

        while True:
            # Ask each demands by ViewForm then create a tournament with user's values
            my_demands = self.view_form.show_form(my_demands)
            new_tournament = MTournament(0,
                             my_demands['name']['value'],
                             my_demands['place']['value'],
                             my_demands['date_start']['value'],
                             my_demands['date_end']['value'],
                             my_demands['number_of_rounds']['value'],
                             my_demands['time_control']['value'],
                             my_demands['description']['value'])

            self.view_form.print_titles(True)
            if new_tournament in self.database_tournament.get_all_objects([]):
                self.view_form.print_text(f"Le tournoi {new_tournament.name} de {new_tournament.place} exite déjà")
            else:
                self.database_tournament.add_object(new_tournament)
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

    def list_tournament(self, sorted_by=["name"]):
        """ Show all tournaments sorted with the keys in 'sorted_by' """

        tournaments = self.database_tournament.get_all_objects(sorted_by)

        text = str()
        for t in tournaments:
            text += f" - {t}\n"

        self.view_form.print_titles(True)
        self.view_form.print_text(text)


if __name__ == "__main__":

    my_titles = Title("Titre d'essai")
    my_titles.update_subtitle("Sous titre d'essai aussi")
    my_controler = ControllerTournament(my_titles)
    #print(my_controler.selection_tournament())
    my_controler.list_tournament()
    #my_controler.create_tournament()

