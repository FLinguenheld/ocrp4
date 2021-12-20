#! env/bin/python3
""" Allow to print titles, texts and a form the terminal """
from os import getcwd
from sys import path
path.insert(1, getcwd())

from copy import deepcopy
from enum import Enum
from datetime import datetime

from view.viewbase import VBase
from view.title import Title
from view.title import _Line


class FormatData(Enum):
    """ Enum for form """
    INT = 0
    STR = 1
    DATE = 2
    UINT = 3
    FLOAT = 4
    LIST = 5
    LISTINT = 6


class VForm(VBase):
    """ Class to show and fill a form in the terminal """

    def __init__(self, titles):
        super().__init__(titles)

    def show_form(self, demands):
        """ Show the titles and the form and ask user for each line.
            To change titles use direct access to "titles" or the method update_subtitle()
            
            demands must be a dict of dicts :
            {"dict1" : {"name" : "…", "format" : FormatData.INT}, 
             "dict2" : {"name" : "…", "format" : FormatData.LIST, "choices" :
                                            ("choices1", "choices2", …)}, … }
            
            The Method will return a copy of this dict of dicts with a new field 'value'
                (it could be exist before and will be erase)
            The field 'choices' is use for FormatData.LIST and FormatData.LISTINT :
                User will have to enter one of these 'choices'

            Attrs:
            - titles (list)
            - demands (dict{dict1, dict2, …})

            Returns:
              new list of dicts demands with 'values' completed
        """

        while True:
            # Copie to restart without answers if ask by user
            copy_demands = deepcopy(demands) 

            for d in copy_demands.values():
                while True:
                    self._refresh(copy_demands)
                    try:
                        new_val = self._ask(d)
                        d['value'] = new_val
                    except KeyboardInterrupt:
                        exit()
                    except:
                        pass
                    else:
                        break

            self._refresh(copy_demands)
            confirmation_text = self.line.formated_text_only_left_side(self.STARS_NUMBER,
                                     "Confirmer le formulaire ? (O)ui / (N)on / (A)bandonner  > ")
            confirmation = input(confirmation_text).upper()

            if confirmation == "O" or confirmation == "OUI":
                return copy_demands
            elif confirmation == "A" or confirmation == "ABANDONNER":
                return None

    def _refresh(self, temp_demands):
        """ Private, used to refresh the form
            It clears the terminal, prints the titles and prints
            the form with the dictionary 'demands' """
        super().print_titles(clear_before=True)
        super().print_line_break()

        for d in temp_demands.values():
            if 'value' not in d.keys() or d['value'] is None: 
                print(self.line.format_text(self.STARS_NUMBER, f"- {d['name']} : ", False))
            else:
                print(self.line.format_text(self.STARS_NUMBER,
                                            f"- {d['name']} : {d['value']}",
                                            False))
        super().print_line_break()

    def _ask(self, demand_in_progress):
        """ Private, according to the 'demand_in_progress['format']',
            ask an question to user and applies a rule to cast the answer 
            Raise an error if cast fail or return the value with the right format

            Attrs :
            - demand_in_progress (dict)

            Returns:
            - Value with good type
        """
        if demand_in_progress['format'] == FormatData.INT:
            new_val = int(self._input(f"{demand_in_progress['name']} ? (nombre) > "))
        
        elif demand_in_progress['format'] == FormatData.UINT:
            new_val = int(self._input(f"{demand_in_progress['name']} ? (nombre positif) > "))
            if new_val < 0:
                raise ValueError
        
        elif demand_in_progress['format'] == FormatData.FLOAT:
            new_val = float(self._input(f"{demand_in_progress['name']} ? (nombre à virgule) > "))
        
        elif demand_in_progress['format'] == FormatData.STR:
            new_val = self._input(f"{demand_in_progress['name']} ? > ")
            if not new_val:
                raise ValueError
        
        elif demand_in_progress['format'] == FormatData.DATE:
            txt = self._input(f"{demand_in_progress['name']} ? (jj/mm/yyyy) > ")
            new_val = str(datetime.strptime(txt, "%d/%m/%Y").strftime("%d/%m/%Y"))

        elif demand_in_progress['format'] == FormatData.LIST:
            new_val = self._input(f"{demand_in_progress['name']} ? " \
                                  f"({' / '.join(demand_in_progress['choices'])}) > ")

            if new_val not in demand_in_progress['choices']:
                raise ValueError

        else:                   # demand_in_progress['format'] == Format.LISTINT 
            new_val = int(self._input(f"{demand_in_progress['name']} ? "\
                                      f"{demand_in_progress['choices']} > "))

            if new_val not in demand_in_progress['choices']:
                raise ValueError

        return new_val

    def _input(self, text):
        """ Formats the text and asks an input (only use in '_ask()') """
        return input(self.line.formated_text_only_left_side(self.STARS_NUMBER, text))


if __name__ == "__main__":

    my_titles = Title("Super titre !!!!!")
    my_titles.update_subtitle("Sous titre encore mieux")
    my_dem = {"name" : {"name" : "Nom", "format" : FormatData.STR},
              "nb_of_tooth" : {"name" : "Nombre de dents", "format" : FormatData.UINT},
              "nb_of_round" : {"name" : "Nombre de rounds", "format" : 
                                    FormatData.LISTINT, "choices" : (2, 4, 8, 16, 20)},
              "birthday" : {"name" : "Date de naissance", "format" : FormatData.DATE},
              "sex" : {"name" : "Sexe", "format" : FormatData.LIST, "choices" :
                                                    ("Masculin", "Féminin", "Autre")}}

    my_form = VForm(my_titles)
    my_form.show_form(my_dem)

