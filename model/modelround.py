#! env/bin/python3
from os import getcwd
from sys import path
path.insert(1, getcwd())

from datetime import datetime

from model.modelbase import MBase

class MRound(MBase):

    def __init__(self, key=0, name="", matches_keys=[]):
        super().__init__(key, name)
        self.matches_keys = matches_keys
        self.datetime_start = None 
        self.datetime_end = None

    def save_datetime_start(self):
        """ Save the current datetime in string for datetime_start """
        self.datetime_start = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

    def save_datetime_end(self):
        """ Save the current datetime in string for datetime_end """
        self.datetime_end = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

    def __str__(self):
        txt = f"{self.name}"
        if self.datetime_start:
            txt += f" - {self.datetime_start}"
        if self.datetime_end:
            txt += f" - {self.datetime_end}"

        return txt

    def __repr__(self):
        return f"Round:"\
                f" key : {self.key}"\
                f" name : {self.name}"\
                f" matches_keys : {self.matches_keys}"\
                f" datetime_start : {self.datetime_start}"\
                f" datetime_end : {self.datetime_end}"


if __name__ == "__main__":
    my_round = MRound(25413, "Round 1", [20164, 3216])
    print(my_round)

    my_round.save_datetime_start()
    print(my_round)

    my_round.save_datetime_end()
    print(my_round)

