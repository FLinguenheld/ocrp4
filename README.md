# ocrp4
OpenClassRooms Projet 4  
Développez un programme logiciel en Python - ChessManager  

![Logo FLinguenheld](https://github.com/FLinguenheld/OpenCR_P2/blob/main/Forelif.png "Pouet")
****
### Installation
Rendez vous dans le dossier de votre choix puis lancez un terminal.  
Clonez le dossier depuis GitHub avec la commande :  
>git clone https://github.com/FLinguenheld/ocrp4 

Installez l'environnement virtuel :
>python3 -m venv env

Activez le :
>source env/bin/activate

Installez les paquets nécessaires à l'aide du fichier requirements.txt :
>pip install -r requirements.txt

Lancez le programme :
>./chessManager.py
****
### Déroulement
Le programme affiche un menu permettant de :
+ Créer un nouveau tournoi
+ Reprendre un des tournois en cours
+ Créer/Modifier des joueurs
+ Mettre à jour le classement ELO
+ Afficher la liste des joueurs
+ Afficher l'historique des tournois


Chaque tournoi est aujourd'hui constitué de 8 joueurs et 4 rounds.
Après la création du tournoi, le programme vous demande de sélectionner les joueurs.  
Il lance ensuite la création du premier round et des matchs avec le système suisse.


Le menu affiche les matchs du round et vous permet de renseigner les résultats.
Une fois tous les matchs renseignés, vous devez valider le round (attention les résultats  
ne seront plus modifiables).
Les scores des joueurs sont mis à jour et le round suivant est généré.


Le programme enregistre la progression du tournoi en cours à chaque modification.  
Vous pouvez le quitter puis le reprendre plus tard en vous rendant dans le menu 'Reprendre tournoi'.  

Vous pouvez également créer et gérer plusieurs tournois simultanément, la liste des tournois non terminés  
est affichée pour vous permettre la sélection.
Un tournoi est automatiquement déclaré terminé lors de la validation du dernier round.


Le menu 'Gestion des joueurs' vous permet de créer, modifier ou d'actualiser le classement ELO d'un joueur.  
Ainsi que d'afficher leur liste avec différentes options de tri.


Vous avez enfin la possibilité d'afficher le classement et le résumé de tous les matchs du tournoi en cours  
ainsi que tous ceux terminés dans l'historique.
****
### Premiers pas
Afin de pouvoir faire des essais lors de la première utilisation du programme, des joueurs et des tournois sont déjà exitants  
dans la base de données.

Si vous souhaitez les supprimer, vous pouvez réinitialiser les sauvegardes. Rendez-vous dans le dossier __sauvegardes__ puis  
supprimez les fichiers suivants :

- players.json
- matchs.json
- rounds.json
- tournaments.json
****
### PEP 8
L'ensemble du code est conforme aux directives PEP 8 comme indiqué dans le fichier html __/flake8_rapport/index.html__.

Vous pouvez générer un nouveau rapport flake8 en suivant ces étapes :

Ouvrez un terminal, rendez vous dans le dossier où vous avez rangé __chessManager.py__, puis activez l'environnement virtuel :
>source env/bin/activate

Cet environnement contient le module flake8. Pour générer un nouveau rapport html, exécutez la commande suivante :
>flake8 --format=html --htmldir=flake8_rapport

Rendez-vous ensuite dans le dossier __flake8_rapport__ et ouvrez le fichier __index.html__ dans votre navigateur web pour afficher  
les résultats du contrôle.
****
### Premiers pas
