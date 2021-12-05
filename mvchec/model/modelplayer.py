#! env/bin/python3

from modelbase import Base

class Player(Base):

    def __init__(self, key=0, name="", last_name="", birth="", sex="", rank=0):
        super().__init__(key, name)
        self.last_name = last_name
        self.birth = birth
        self.sex = sex
        self.rank = rank

    def __str__(self):
        return f"""Joueur :
        key : {self.key}
        prénom : {self.name}
        nom : {self.last_name}
        date de naissance : {self.birth}
        sexe : {self.sex}
        rang : {self.rank}"""

   # Sérialisation… 
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

    my_model = Player(54664, "Jean", "Dupont", "1999-02-20", "Masculin", 12)
    print(my_model)
