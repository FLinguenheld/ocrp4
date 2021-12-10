#! env/bin/python3
from os import getcwd
from sys import path
path.insert(1, getcwd())


from model.modelbase import MBase
 

class MTournament(MBase):

    def __init__(self, key=0, name="", place="", date_start=None, date_end=None,
                number_of_rounds=4, time_control="", description=""):
        super().__init__(key, name)
        self.place = place
        self.date_start = date_start 
        self.date_end = date_end
        self.number_of_rounds = number_of_rounds
        self.round_keys = []
        self.player_keys = []
        self.time_control = time_control
        self.description = description

    def __str__(self):
        return f"{self.name}"\
        f" de {self.place}"\
        f" du {self.date_start}"\
        f" au {self.date_end}"\
        f" - {self.description}"

    def __repr__(self):
        return f"Tournoi :"\
        f" key : {self.key}"\
        f" nom : {self.name}"\
        f" round_keys : {self.round_keys}"\
        f" player_keys : {self.player_keys}"

    def serialize(self):
        dict_to_serialize = super().serialize()
        dict_to_serialize["place"] = self.place
        dict_to_serialize["date_start"] = self.date_start
        dict_to_serialize["date_end"] = self.date_end
        dict_to_serialize["number_of_rounds"] = self.number_of_rounds
        dict_to_serialize["round_keys"] = self.round_keys
        dict_to_serialize["player_keys"] = self.player_keys
        dict_to_serialize["time_control"] = self.time_control
        dict_to_serialize["description"] = self.description

        return dict_to_serialize

    def unserialize(self, values):
        super().unserialize(values)
        self.place = values["place"]
        self.date_start = values["date_start"]
        self.date_end = values["date_end"]
        self.number_of_rounds = values["number_of_rounds"]
        self.round_keys = values["round_keys"]
        self.player_keys = values["player_keys"]
        self.time_control = values["time_control"]
        self.description = values["description"]

    def __eq__(self, other_tournament):
        """ Compare two tournaments (name/place/date_start/date_end/number_of_rounds/time_control) """
        return (self.name == other_tournament.place
                and self.place == other_tournament.place
                and self.date_start == other_tournament.date_start
                and self.date_end == other_tournament.date_end
                and self.number_of_rounds == other_tournament.number_of_rounds
                and self.time_control == other_tournament.time_control)


if __name__ == "__main__":
    my_tournament = MTournament(10, "Tournoi génial", "Villebon")
    print(my_tournament)
