#! env/bin/python3
""" Model to represent a player """
from os import getcwd
from sys import path
path.insert(1, getcwd())

from model.modelbase import MBase
 

class MPlayer(MBase):

    def __init__(self, key=0, name="", last_name="", birth="", sex="", rank=0):
        super().__init__(key, name)
        self.last_name = last_name
        self.birth = birth
        self.sex = sex
        self.rank = rank
        # Points is a temporary save
        self.points = 0

    @property
    def complete_name(self):
        return f"{self.name} {self.last_name}"

    def __str__(self):
        return f"{self.name} {self.last_name}"\
        f" né le {self.birth}"\
        f" - {self.sex}"\
        f" - rang : {self.rank}"

    def __repr__(self):
        return f"Player:"\
        f" key : {self.key}"\
        f" prénom : {self.name}"\
        f" nom : {self.last_name}"\
        f" date de naissance : {self.birth}"\
        f" sexe : {self.sex}"\
        f" rang : {self.rank}"

    def serialize(self):
        dict_to_serialize = super().serialize()
        dict_to_serialize["last_name"] = self.last_name
        dict_to_serialize["birth"] = self.birth
        dict_to_serialize["sex"] = self.sex
        dict_to_serialize["rank"] = self.rank

        return dict_to_serialize

    def unserialize(self, values):
        super().unserialize(values)
        self.last_name = values["last_name"]
        self.birth = values["birth"]
        self.sex = values["sex"]
        self.rank = values["rank"]
        
    def __eq__(self, other_player):
        """ Compare all parts of two players without their keys """
        return (self.name == other_player.name
                and self.last_name == other_player.last_name
                and self.birth == other_player.birth
                and self.sex == other_player.sex)


if __name__ == "__main__":

    my_model = MPlayer(54664, "Jean", "Dupont", "1999-02-20", "Masculin", {105:1, 5:3})
    print(my_model)
