#! env/bin/python3

from copy import deepcopy
from viewbase import VBase

class VMenu(VBase):
    """ This class allow to show a menu and wait a reponse from the user.
        To change titles use direct access to "titles" or the method update_subtitle()

        Choices must be a dict() like this :
        (you can use a letter for key to create a space in menu - this line will be ignored)
            {1:"Choice 1", 2:"Choice 2", "a":None, 3:"Choice 3", …}

            1 - Choice 1
            2 - Choice 2
            
            3 - Choice 3
        …
    """
    def __init__(self, titles, line_length=100):
        super().__init__(titles, line_length)
        self.menu = _Menu()

    def show_menu(self, choices, number_of_choices=1):
        """ Show a menu, wait and return the user's choice (int).
            choices (dict{int:str}) : Represent the possibilities (see Menu class for details)"""
       
        user_choices = []
        self.menu.update_choices(choices)
        self._refresh()

        for i in range(number_of_choices):

            while True:
                try:
                    if number_of_choices == 1 :
                        question = "Sélection ? > "
                    else:
                        question = f"Sélection {i}/{number_of_choices} ? > "

                    current_choice = int(input(question))

                    if isinstance(current_choice, int) and current_choice in self.menu:
                        user_choices.append(current_choice)

                        # Change the selected ke keyy in negative (it will print with an other style by _Menu)
                        self.menu.choices = {float(current_choice) if k == current_choice else k:v for k, v in self.menu.choices.items()}
                        self._refresh()
                        break
                    else:
                        raise ValueError

                except KeyboardInterrupt:
                    exit()
                except:
                    self._refresh()
                    print(f"Ce choix n'est pas possible")

    def _refresh(self):
        """ Clear the terminal, print titles and the menu """
        super().print_titles()
        print(self.menu)


class _Menu:
    """ Allow to create a menu in terminal.
        Use update_choices() to create a new menu and print to show the menu
        The equal symbol could be use to test if the index exists in menu.

        In 'choices' the keys in string are ignored, the keys in float are considered 'selected'
        and int are print normaly.
        See VMenu to read an exemple for the dictionary 'choices'
    """
    def __init__(self):
        self.choices = {}

    def update_choices(self, choices):
        """ Made a copy of choices, use this attribute to change int keys in float """
        self.choices = deepcopy(choices)

    def __str__(self):
        txt = str()
        for k, v in self.choices.items():
            if isinstance(k, int):
                txt += f"   {k} : {v}\n"
            elif isinstance(k, float):
                txt += f"       -> {int(k)} : {v}\n"
            else:
                txt += "\n"
        return txt

    def __contains__(self, index):
        """ Allow to use = to check if index (int) exists in self.choices' keys
            Ignore all non-int keys """
        keys_int_only = [k for k in self.choices.keys() if isinstance(k, int)]
        return isinstance(index, int) and index in keys_int_only 


if __name__ == "__main__":

    my_titles = ["Titre 1", "Titre 2", "Titre 3"]
    my_choices = {1:"Choix 1", 2:"Choix 2", "a":None, 3:"Choix 3", "b":None, 4:"Choix 4"}

    test = VMenu(my_titles, 50)
    test.show_menu(my_choices, 3)
