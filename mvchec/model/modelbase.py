#! env/bin/python3

class Base:

    def __init__(self, name,):
        self.name = name

    def __str__(self):
        return f"Model base - name : {self.name}"

    def serialize(self):
        return {"name" : self.name}
    
    def unserialize(self, values):
        self.name = values["name"]

if __name__ == "__main__":

    my_model = Base("test")
    print(my_model)
