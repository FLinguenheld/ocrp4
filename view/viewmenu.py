#! env/bin/python3
""" Allow to print titles, texts and a menu in the terminal """
from os import getcwd
from sys import path
path.insert(1, getcwd())

from copy import deepcopy
from view.viewbase import VBase
from view.title import Title
from view.title import _Line


class VMenu(VBase):
    """ This class allow to show a menu and wait a reponse from the user.

        Choices must be a dict() like this :
        (you can use a letter for key to create a space in menu - this line will be ignored)
            {1:"Choice 1", 2:"Choice 2", "a":None, 3:"Choice 3", …}

            1 - Choice 1
            2 - Choice 2

            3 - Choice 3
            …
    """

    def __init__(self, titles):
        super().__init__(titles)
        self.menu = _Menu(titles.length, self.STARS_NUMBER)

    def show_menu(self, choices, number_of_choices=1):
        """ Show a menu, wait and return the user's choice (int).
            choices (dict{int:str}) : Represent the possibilities (see Menu class for details)

            Retun a list with the choices (int)
            or just an int if only one choice asked """

        user_choices = []
        self.menu.update_choices(choices)
        self._refresh()

        for i in range(number_of_choices):

            while True:
                try:
                    if number_of_choices == 1:
                        question = self.line.formated_text_only_left_side(self.STARS_NUMBER,
                                                                          "Sélection ? > ")
                    else:
                        question = self.line.formated_text_only_left_side(self.STARS_NUMBER,
                                                                          f"Sélection {i}/{number_of_choices} ? > ")

                    current_choice = int(input(question))

                    if isinstance(current_choice, int) and current_choice in self.menu:
                        user_choices.append(current_choice)

                        # Change the selected key in float
                        # (it will print with an other style by _Menu)
                        self.menu.choices = {
                            float(current_choice) if k == current_choice else k: v for k,
                            v in self.menu.choices.items()}
                        self._refresh()
                        break
                    else:
                        raise ValueError

                except KeyboardInterrupt:
                    exit()
                except BaseException:
                    self._refresh()
                    print(self.line.formated_text_only_left_side(self.STARS_NUMBER,
                                                                 "Ce choix n'est pas possible"))

        if number_of_choices == 1:
            return user_choices[0]
        else:
            return user_choices

    def _refresh(self):
        """ Clear the terminal, print titles and the menu """
        super().print_titles()
        super().print_line_break()
        self.menu.print()
        super().print_line_break()


class _Menu:
    """ Allow to create a menu in terminal.
        Use update_choices() to create a new menu and print to show the menu
        The equal symbol could be use to test if the index exists in menu.

        In 'choices' the keys in string are ignored, the keys in float are considered 'selected'
        and int are print normaly.
        See VMenu to read an exemple for the dictionary 'choices'
    """

    def __init__(self, line_length, stars_number):
        self.choices = {}
        self.line = _Line(line_length)
        self.STARS_NUMBER = stars_number

    def update_choices(self, choices):
        """ Made a copy of choices, use this attribute to change int keys in float """
        self.choices = deepcopy(choices)

    def print(self):
        """ Print line by line the menu """
        for k, v in self.choices.items():
            if isinstance(k, int):
                print(self.line.format_text(self.STARS_NUMBER, f"{k} : {v}", False))

            elif isinstance(k, float):
                print(self.line.format_text(self.STARS_NUMBER, f"     -> {int(k)} : {v}", False))

            else:
                print(self.line.formated_jump(self.STARS_NUMBER))

    def __contains__(self, index):
        """ Allow to use = to check if index (int) exists in self.choices' keys
            Ignore all non-int keys """
        keys_int_only = [k for k in self.choices.keys() if isinstance(k, int)]
        return isinstance(index, int) and index in keys_int_only


if __name__ == "__main__":

    my_titles = Title("Super titre !!!!!")
    my_titles.update_subtitle("Sous titre encore mieux")
    my_choices = {1: "Choix 1", 2: "Choix 2", "a": None, 3: "Choix 3", "b": None, 4: "Choix 4"}

    test = VMenu(my_titles)
    user_choices = test.show_menu(my_choices, 3)
    print(user_choices)
