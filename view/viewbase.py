#! env/bin/python3
""" Base for views, regroups main attributes and methods """
from os import getcwd
from sys import path
path.insert(1, getcwd())

from os import system
from os import name

from view.title import SubtitleLevel
from view.title import Title
from view.title import _Line
from view.title import _Separator


class VBase:
    """ Mother for views in the terminal
        Includes methods to clear or add text in terminal

        All textes are formated with the class _Line
        It allows to uniform lines with stars *

        Titles are managed with the class 'Title'. Give a title object in constructor
        update him and use 'print_titles()' here to clear terminal and print titles
    """

    def __init__(self, titles):
        self.titles = titles
        self.separator = _Separator(titles.length)

        self.line = _Line(titles.length)
        self.STARS_NUMBER = 2

    def ask_confirmation(self, text):
        """ Clear the screen, print the titles and ask a confirmation
            Retun a bool according the user's choice """

        while True:
            self.print_titles()
            self.print_line_break()
            self.print_text(text, ask_to_continue=False)
            self.print_line_break()
            answer = input(self.line.formated_text_only_left_side(self.STARS_NUMBER,
                                                                  "Confirmer ? O/N > "))

            if answer.upper() == "O" or answer.upper() == "OUI":
                return True
            elif answer.upper() == "N" or answer.upper() == "NON":
                return False

    def print_text(self, text, ask_to_continue=True, center=False):
        """ Print a text or a list of text and wait a key to continue

            Attrs:
            - text (str or list(str))   text to print
            - center (bool):            used to center the text """

        if isinstance(text, str):
            print(self.line.format_text(self.STARS_NUMBER, text, center))
        else:
            for t in text:
                print(self.line.format_text(self.STARS_NUMBER, t, center))

        if ask_to_continue:
            self.print_line_break()
            input(self.line.formated_text_only_left_side(self.STARS_NUMBER,
                                                         "Appuyez sur une touche pour continuer..."))

    def clear_terminal(self):
        """ Clear the terminal """
        system("cls" if name == "nt" else "clear")

    def print_titles(self, clear_before=True):
        """ Print the titles (see class Title for details) """
        if clear_before:
            self.clear_terminal()

        self.titles.print()

    def print_line_break(self):
        """ Print a break line """
        print(self.line.formated_jump(self.STARS_NUMBER))

    def print_separator(self):
        """ Print a separator (see class Separator for details)
            The length was specified in the constructor """
        print(self.separator)


if __name__ == "__main__":

    my_titles = Title("titre 1")
    my_view = VBase(my_titles)

    my_titles.update_subtitle("youhou !!\nC'est tropppp\nCOoooool", SubtitleLevel.FIRST)
    my_titles.update_subtitle("pouet !", SubtitleLevel.THIRD)
    my_view.print_titles()

    my_view.print_line_break()
    my_text = "Bonjour à tous !"
    my_view.print_text(my_text, True)

    my_view.print_line_break()
    my_view.print_text("Alors\nVous allez\nBieN ?", ask_to_continue=False)

    my_view.print_separator()

    my_text_list = ["Et", "une", "bonne ou très bonne", "journée", "bien", "sûr"]
    my_view.print_text(my_text_list, True, True)
