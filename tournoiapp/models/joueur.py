class Joueur:
    def __init__(self, nom, niveau):
        self.nom = nom
        self.niveau = niveau
        self.points = 0
        self.buts_pour = 0
        self.buts_contre = 0

    def choisir_equipe(self, equipe):
        self.equipe = equipe

    def enregistrer_resultat(self, buts_pour, buts_contre):
        self.buts_pour += buts_pour
        self.buts_contre += buts_contre
        if buts_pour > buts_contre:
            self.points += 3
        elif buts_pour == buts_contre:
            self.points += 1

    @property
    def difference_buts(self):
        return self.buts_pour - self.buts_contre
    
    def __repr__(self):
        return f'{self.nom}'