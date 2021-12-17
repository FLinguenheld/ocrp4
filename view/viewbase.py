#! env/bin/python3
from os import getcwd
from sys import path
path.insert(1, getcwd())

from os import system
from os import name
from enum import Enum


class VBase:
    """ Mother for views in the terminal
        Includes methods to clear or add text in terminal

        Titles are managed with the class 'Title'. Give a title object in constructor
        update him and use 'print_titles()' here to clear terminal and show titles
    """

    def __init__(self, titles):
        self.titles = titles
        self.line_length = titles.length

    def ask_confirmation(self, text):
        """ Clear the screen, print the titles and ask a confirmation
            Retun a bool according the user's choice """ 

        while True:
            self.print_titles()
            print(f"\n{text}\n")
            answer = input("Confirmer ? O/N > ") 

            if answer.upper() == "O" or answer.upper() == "OUI":
                return True
            elif answer.upper() == "N" or answer.upper() == "NON":
                return False

    def print_text(self, text, ask_to_continue=True, center=False):
        """ Print a text or a list of text and wait a key to continue

            Attrs:
            - text (str or list(str))   text to print
            - center (bool):            used to center the text """

        formated_text = str()
        if isinstance(text, str):
            if center:
                formated_text = text.center(self.line_length) + "\n"
            else:
                formated_text = text + "\n"
        else:
            for t in text:
                if center:
                    formated_text += t.center(self.line_length) + "\n"
                else:
                    formated_text += t + "\n"

        print(formated_text)

        if ask_to_continue:
            input("\nAppuyez sur une touche pour continuer...")

    def clear_terminal(self):
        """ Clear the terminal """
        system("cls" if name == "nt" else "clear")

    def print_titles(self, clear_before=True):
        """ Print the titles (see class Title for details) """
        if clear_before:
            self.clear_terminal()

        print(self.titles)

    def print_line_break(self):
        """ Print a break line """
        print("\n")

    def print_separator(self):
        """ Print a separator (see class Separator for details)
            The length was specified in the constructor """
        print(Separator(self.line_length))


class SubtitleLevel(Enum):
    """ Values are used for the stars in texts """
    FIRST=4
    SECOND=3
    THIRD=2
    FOURTH=1
    ALL=10


class Title:
    """ Class to represent a title or a list of title in terminal
        Create an objet and use it with print()
        *************
            title
        *************
          subtitle1
        *************

        Attrs:
            - titles (list)     : list of titles
            - line_length (int) : line length in number of caracters

    """
    def __init__(self, title, line_length=100):
        self.title = title
        self.length = line_length
        self.separator = Separator(line_length)
        self.subtitles = {4:'', 3:'', 2:'', 1:''}

        self.star_multiplier = 3
        self.stars_nb_for_title = 5

    def update_subtitle(self, text, level=SubtitleLevel.FIRST):
        """ Update de subtitle text at the indicated level """
        if level != SubtitleLevel.ALL:
            self.subtitles[level.value] = text
    
    def clear_subtitle(self, level=SubtitleLevel.FIRST):
        """ Clear the subtitle at the indicated level (All to complete clear) """
        if level == SubtitleLevel.ALL:
            for k in self.subtitles.keys():
                self.subtitles[k] = ''
        else:
            self.subtitles[level.value] = ''

    def __str__(self):
        # Nb of stars is calculate with the enum value and 'self.star_multiplier'
        txt = str(self.separator)
        txt += self._format_text(self.title, self.stars_nb_for_title * self.star_multiplier) + "\n"
        txt += str(self.separator)

        for k, v in self.subtitles.items():
            if v:
                for line in v.split("\n"):
                    txt += self._format_text(line, k * self.star_multiplier) + "\n"

                txt += str(self.separator)

        return txt

    def __repr__(self):
        return f"{self.title} - {self.subtitles}"

    def _format_text(self, txt, nb_stars):
        """ Add stars to text for a beautifull effect ^^ """
        length_without_stars = self.length - (nb_stars * 2)
        return "*" * nb_stars + txt.center(length_without_stars) + "*" * nb_stars


class Separator:
    """ Class to represent a separator (a stars line)
        Define the length in constructor and use print()
    """
    def __init__(self, length):
        self.length = length

    def __str__(self):
        return "*" * self.length + "\n"


if __name__ == "__main__":

    my_titles = Title("titre 1")
    my_view = VBase(my_titles)

    my_titles.update_subtitle("youhou !!\nC'est tropppp\nCOoooool", SubtitleLevel.FIRST)
    my_titles.update_subtitle("pouet !", SubtitleLevel.THIRD)
    my_view.print_titles()

    my_text = "Bonjour à tous !"
    my_view.print_text(my_text, True)

    my_view.print_separator()

    my_text_list = ["Et", "une", "bonne ou très bonne", "journée", "bien", "sûr"]
    my_view.print_text(my_text_list, True, True)
