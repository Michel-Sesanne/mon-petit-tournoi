from tournoiapp.models import Calendrier
from typing import Optional

class Poule:
    def __init__(self, nom, joueurs):
        self.nom = nom
        self.joueurs = joueurs
        self.nb_joueurs = len(joueurs)
        self.matchs = []
        self.calendrier: Optional[Calendrier] = None

    def generer_calendrier(self):
        calendrier = Calendrier(self.matchs)    # Création de l'objet Calendrier associé à la poule
        nom_methode = f"mode_poule_{self.nb_joueurs}_joueurs"   # Nom de la méthode à appeler dynamiquement
        methode = getattr(calendrier, nom_methode, None)    # Récupération de la méthode dans l'instance `calendrier`
        if not methode:
            raise ValueError(f"Calendrier non supporté pour {self.nb_joueurs} joueurs.")
        methode()   # Appel de la méthode qui modifie l'objet `calendrier`
        self.calendrier = calendrier    # Stockage de l'objet configuré
        
    def classement(self):
        stats = {j: {"points": 0, "but_pour": 0, "but_contre": 0} for j in self.joueurs}

        for match in self.matchs:
            if match.score_j1 is None or match.score_j2 is None:
                continue
            stats[match.joueur1]["but_pour"] += match.score_j1
            stats[match.joueur1]["but_contre"] += match.score_j2
            stats[match.joueur2]["but_pour"] += match.score_j2
            stats[match.joueur2]["but_contre"] += match.score_j1

            if match.vainqueur is None:
                stats[match.joueur1]["points"] += 1
                stats[match.joueur2]["points"] += 1
            else:
                stats[match.vainqueur]["points"] += 3

        def key(joueur):
            s = stats[joueur]
            diff = s["but_pour"] - s["but_contre"]
            coef = joueur.niveau
            return (s["points"], diff, s["but_pour"], coef)

        return sorted(self.joueurs, key=key, reverse=True), stats

    def qualifies(self, nb_qualifies):
        classement, _ = self.classement()
        return classement[:nb_qualifies]
    
    def __repr__(self):
        classement, stats = self.classement()
        lignes = ["\nPos |   Joueur   |Points| Diff | BP | BC"]
        for i, j in enumerate(classement, 1):
            s = stats[j]
            diff = s["but_pour"] - s["but_contre"]
            str_diff = f"{'+' if diff > 0 else ''}{diff}"
            diff_aff = f"{str_diff:^4}"
            lignes.append(
                f"{i:^3} | {j.nom:<10} | {s['points']:^4} | {diff_aff} | {s['but_pour']:<2} | {s['but_contre']:<2}"
            )
        return "\n".join(lignes)