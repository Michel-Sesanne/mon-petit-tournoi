class Match:
    def __init__(self, joueur1, joueur2):
        self.joueur1 = joueur1
        self.joueur2 = joueur2
        self.score_j1 = None
        self.score_j2 = None
        self.termine = False

    def enregistrer_resultat(self, score_j1, score_j2):
        self.score_j1 = score_j1
        self.score_j2 = score_j2
        self.termine = True

    @property
    def vainqueur(self):
        if self.score_j1 is None or self.score_j2 is None:
            return None
        if self.score_j1 > self.score_j2:
            return self.joueur1
        elif self.score_j2 > self.score_j1:
            return self.joueur2
        else:
            return None  # Match nul        

    def __repr__(self):
        if not self.termine:
            return f"{self.joueur1.nom} - {self.joueur2.nom} (A venir)"        
        return f"{self.joueur1.nom} - {self.joueur2.nom} : {self.score_j1}-{self.score_j2}"
    
class MatchKO(Match):
    def __init__(self, joueur1, joueur2):
        super().__init__(joueur1, joueur2)
        self.phase = 'eliminatoire'

    def enregistrer_resultat(self, score_j1, score_j2, prolong_j1=None, prolong_j2=None, tirs_j1=None, tirs_j2=None):
        super().enregistrer_resultat(score_j1, score_j2)
        if score_j1 != score_j2:
            self.prolong_j1 = None
            self.prolong_j2 = None
            self.tirs_j1 = None
            self.tirs_j2 = None
        else:            
            self.prolong_j1 = prolong_j1
            self.prolong_j2 = prolong_j2
            self.tirs_j1 = tirs_j1
            self.tirs_j2 = tirs_j2
        if self.vainqueur is None and self.termine:
            raise ValueError("Match terminé mais aucun vainqueur déterminé !")

    @property
    def vainqueur(self):
        vainqueur = super().vainqueur
        if vainqueur is not None:
            return vainqueur
        else:
            # Égalité après le temps réglementaire
            if self.prolong_j1 is not None and self.prolong_j2 is not None:
                if self.prolong_j1 > self.prolong_j2:
                    return self.joueur1
                elif self.prolong_j2 > self.prolong_j1:
                    return self.joueur2
            if self.tirs_j1 is not None and self.tirs_j2 is not None:
                if self.tirs_j1 > self.tirs_j2:
                    return self.joueur1
                elif self.tirs_j2 > self.tirs_j1:
                    return self.joueur2
        return None # Match nul (ne devrait pas arriver en KO)

    def __repr__(self):
        base_repr = super().__repr__()
        details = []
        if self.prolong_j1 is not None and self.prolong_j2 is not None:
            details.append(f"Prol.: {self.prolong_j1}-{self.prolong_j2}")
        if self.tirs_j1 is not None and self.tirs_j2 is not None:
            details.append(f"T.a.b: {self.tirs_j1}-{self.tirs_j2}")
        if details:
            return f"{base_repr} ({', '.join(details)})"
        return base_repr