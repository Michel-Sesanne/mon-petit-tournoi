class Chapeau:
    def __init__(self, numero):
        self.numero = numero
        self.joueurs = []

    def ajouter_joueur(self, joueur):
        self.joueurs.append(joueur)

    def __repr__(self):
        joueurs_str = ', '.join([f'{joueur.nom} ({joueur.equipe})' for joueur in self.joueurs])
        return f'Chapeau {self.numero} : {joueurs_str}'