#! env/bin/python3

from tinydb import TinyDB, Query
from random import randint

from view.viewform import VForm
from view.viewform import FormatData
from view.viewmenu import VMenu


class ControllerBase:

    def __init__(self, database_name):
        self.data_base = TinyDB(database_name)
        self.query = Query()

        self.titles = ["GESTIONNAIRE DE TOURNOI D'ECHECS (à modifier)"]
        self.view_form = VForm(self.titles)
        self.view_menu = VMenu(self.titles)

    def _generate_key(self):
        """ Generate a unique key in the tinydb opened by __init__ """
        while True:
            new_key = randint(10, 9999999)

            if not self.element_by_key(self):
                return new_key

    def element_by_key(self, key):
        """ Return the element in the data base with the key mentioned """
        return self.data_base.search(self.query.key == key)

    def elements_sorted(self, sort_keys):
        """ Return all data base sorted with the list sort_keys
            ex : ('name', 'last_name', 'rank', …)"""
        elements = self.data_base.all()
        for k in sort_keys:
            elements = sorted(elements, key=lambda d:d[k])

        return elements


if __name__ == "__main__":
    pass

