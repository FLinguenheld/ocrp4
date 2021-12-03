#! env/bin/python3


from view.viewform import VForm
from view.viewmenu import VMenu
from controlplayer import ControllerPlayer
    
class ControllerMenu:

    def __init__(self):
        self.titles = ["GESTIONNAIRE DE TOURNOI D'ECHECS (à modifier)"]
        self.view_form = VForm(self.titles)
        self.view_menu = VMenu(self.titles)

    def test(self):
        pass


if __name__ == "__main__":

       my_controler = ControllerMenu()
       my_controler.test()
        
