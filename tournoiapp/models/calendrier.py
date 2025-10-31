from .match import Match
from typing import List

class Calendrier:
    def __init__(self, matchs: List[Match]):
        self.matchs = matchs
        self.nb_matchs = len(matchs)
        self.journees = {}     

    def mode_poule_4_joueurs(self):
        self.journees = {}
        for i in range(3):
            self.journees[i + 1] = [self.matchs[j] for j in range(i * 2, (i + 1) * 2)]
    
    def mode_poule_6_joueurs(self):
        self.journees = {}
        for i in range(3):
            self.journees[i + 1] = [self.matchs[j] for j in range(i * 3, (i + 1) * 3)]

    def mode_poule_7_joueurs(self):
        self.journees = {}
        self.journees[1] = [self.matchs[0], self.matchs[1]]
        self.journees[2] = [self.matchs[2], self.matchs[3]]
        self.journees[3] = [self.matchs[4], self.matchs[5], self.matchs[6]]

    def __repr__(self):
        string = ''
        for journee, matchs in self.journees.items():
            string += f'Journée {journee}:\n'
            for match in matchs:
                string += f'  {match}\n'
        return string