#! env/bin/python3
""" Titles, Enum SubtitleLevel, Line and Separator classes used in views """
from os import getcwd
from sys import path
path.insert(1, getcwd())

from enum import Enum


class SubtitleLevel(Enum):
    """ Values are used for the stars in texts """
    FIRST = 4
    SECOND = 3
    THIRD = 2
    FOURTH = 1
    ALL = 10


class Title:
    """ Class to represent a title or a list of title in terminal
        Create an objet and use it with print()
        *************
            title
        *************
          subtitle1
        *************
    """

    def __init__(self, title, line_length=100):
        self.title = title
        self.length = line_length
        self.line = _Line(line_length)

        self.separator = _Separator(line_length)
        self.subtitles = {4: '', 3: '', 2: '', 1: ''}

        self.STARS_MULTIPLIER = 3
        self.STARS_NB_FOR_TITLE = 5

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

    def print(self):
        """ Print titles and subtitles in the terminal """
        print(self.separator)
        # Title
        print(self.line.format_text(self.STARS_NB_FOR_TITLE * self.STARS_MULTIPLIER,
                                    self.title,
                                    center=True))
        print(self.separator)

        # Subtitles
        for k, v in self.subtitles.items():
            if v:
                for line in v.split("\n"):
                    print(self.line.format_text(k * self.STARS_MULTIPLIER,
                                                line,
                                                center=True))
                print(self.separator)

    def __repr__(self):
        return f"{self.title} - {self.subtitles}"


class _Line:
    """ Allow to format text with the same way in the terminal """

    def __init__(self, length):
        self.length = length
        self.TABULATION = 5

    def format_text(self, stars_number, text, center):
        """ Retun a formated text with stars on both sides :
            **       text      **

            You can use a text (with /n) or a list of string
        """
        formated_text = str()
        for line in text.split("\n"):
            if center:
                formated_text += "*" * stars_number
                formated_text += line.center(self.length - (stars_number * 2))
                formated_text += "*" * stars_number
            else:
                formated_text += "*" * stars_number
                formated_text += " " * self.TABULATION
                formated_text += line
                formated_text += " " * (self.length - len(line) - (stars_number * 2) - self.TABULATION)
                formated_text += "*" * stars_number

            formated_text += "\n"

        # Return text without the last \n
        return formated_text[:-1]

    def formated_text_only_left_side(self, stars_number, text):
        """ Specific for input line """
        formated_text = "*" * stars_number
        formated_text += " " * self.TABULATION
        formated_text += text

        return formated_text

    def formated_jump(self, stars_number):
        """ Jump line with stars on both sides """
        return self.format_text(stars_number, " ", True)


class _Separator:
    """ Class to represent a separator (a stars line)
        Define the length in constructor and use print()
    """

    def __init__(self, length):
        self.length = length

    def __str__(self):
        return "*" * self.length
