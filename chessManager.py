#! env/bin/python3

from controller.menu.controlmenumain import ControllerMenuMain

from view.title import Title
from view.title import SubtitleLevel
from view.viewmenu import VMenu

try:

    my_titles = Title("GESTIONNAIRE DE TOURNOIS D'ECHECS", line_length=100)
    my_view = VMenu(my_titles) 

    my_menu = ControllerMenuMain(my_titles)
    my_menu.show()


except KeyboardInterrupt:
    #my_titles.clear_subtitle(SubtitleLevel.ALL)
    #my_titles.update_subtitle("Arrêt")
    #my_view.print_titles()
    #my_view.print_text("À bientôt !", ask_to_continue=False, center=True)
    print("prout")
