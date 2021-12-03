#! env/bin/python3

from modelbase import Base

class Round(Base):

    def __init__(self, players):
        self.players(players)

