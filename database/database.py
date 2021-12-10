#! env/bin/python3

from os import getcwd
from sys import path
path.insert(0, getcwd())

from tinydb import TinyDB, Query
from random import randint

from model.modelbase import MBase


class DBase:

    def __init__(self, database_name):
        self.data_base = TinyDB(database_name)
        self.query = Query()

    def add_object(self, obj):
        """ Create and serialize the new match.
        Return the key generated for the new match """
 
        obj.key = self._generate_key()
        self.data_base.insert(obj.serialize())
        return obj.key

    def update_object(self, obj):
        """ Update the object in the database """
        self.data_base.update(obj.serialize(), self.query.key == obj.key)

    def get_object_by_key(self, key):
        pass

    def _generate_key(self):
        """ Generate a unique key in the tinydb opened by __init__ """
        while True:
            new_key = randint(100, 99999999)

            if not self._dict_by_key(self):
                return new_key

    def _dict_by_key(self, key):
        """ Return the dictionary in the data base with the key mentioned """
        results = self.data_base.search(self.query.key == key)
        if results:
            return results[0]

    def _all_dicts(self, sort_keys):
        """ Return a list with all data base dictionaries sorted with the list sort_keys
            ex : ['name', 'last_name', 'rank', …]"""
        elements = self.data_base.all()
        if sort_keys:
            for k in sort_keys:
                elements = sorted(elements, key=lambda d:d[k])

        return elements


if __name__ == "__main__":
    pass

