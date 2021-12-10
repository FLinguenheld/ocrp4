#! env/bin/python3
from os import getcwd
from sys import path
path.insert(1, getcwd())

from os import system
from os import name


class VBase:
    """ Mother for views in the terminal
        Includes the titles' management and methodes to clear or add text in terminal
    """

    def __init__(self, titles, line_length=100):
        self.titles = titles
        self.line_length = line_length

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

    def update_subtitle(self, new_subtitle):
        """ Allow to easily replace the subtitle without change the title """
        del self.titles[1:]
        self.titles.append(new_subtitle)

    def print_titles(self, clear_before=True):
        """ Print the title (see class Title for details) """
        if clear_before:
            self.clear_terminal()

        print(Title(self.titles, self.line_length))

    def print_line_break(self):
        """ Print a break line """
        print("\n")

    def print_separator(self):
        """ Print a separator (see class Separator for details)
            The length was specified in the constructor """
        print(Separator(self.line_length))


class Title:
    """ Class to represent a title or a list of title in terminal
        Create an objet and use it with print()
        ************
           title1
        ************
           title2
        ************

        Attrs:
            - titles (list)     : list of titles
            - line_length (int) : line length in number of caracters

    """
    def __init__(self, titles, line_length):
        self.titles = titles
        self.length = line_length
        self.separator = Separator(line_length)

    def __str__(self):
        txt = str(self.separator)
        for t in self.titles :
            txt += t.center(self.length) + "\n"
            txt += str(self.separator)

        return txt


class Separator:
    """ Class to represent a separator (a stars line)
        Define the length in constructor and use print()
    """
    def __init__(self, length):
        self.length = length

    def __str__(self):
        return "*" * self.length + "\n"


if __name__ == "__main__":

    my_titles = ["Titre 1", "Titre 2", "Titre 3"]
    my_view = VBase(my_titles)

    my_view.print_titles()

    my_text = "Bonjour à tous !"
    my_view.print_text(my_text, True)

    my_view.print_separator()

    my_text_list = ["Et", "une", "bonne ou très bonne", "journée", "bien", "sûr"]
    my_view.print_text(my_text_list, True)
