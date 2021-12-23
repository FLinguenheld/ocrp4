#! env/bin/python3
""" Base for models, regroups main attributes and methods """


class MBase:

    def __init__(self, key=0, name=''):
        self.key = key
        self.name = name

    def __str__(self):
        return f"Model base - key : {self.key} - name : {self.name}"

    def serialize(self):
        return {"key": self.key, "name": self.name}

    def unserialize(self, values):
        self.key = values["key"]
        self.name = values["name"]


if __name__ == "__main__":
    my_model = MBase(546, "test")
    print(my_model)
