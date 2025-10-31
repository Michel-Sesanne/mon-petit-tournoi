import math
from datetime import date
from typing import List, Optional
from tournoiapp.services import TirageService, CalendrierService
from tournoiapp.models import Chapeau, Joueur, Poule, Match, MatchKO
class Tournoi:
    """
    Représente un tournoi avec ses joueurs, sa structure (poules, chapeaux, phases finales)
    et son état d'avancement.
    """

    def __init__(
        self,
        id: int,
        nom: str,
        date_tournoi: Optional[date] = None,
        joueurs: Optional[List[Joueur]] = None
    ):
        # Informations générales
        self.id = id
        self.nom = nom
        self.date = date_tournoi or date.today()

        # Données des joueurs
        self.joueurs = joueurs or []
        self.nb_joueurs = len(self.joueurs)

        # Logique de structure   
        self.etat = "En préparation"  # Etats possibles : En préparation, Phase de poule, Phase Finale, Terminé
        self.tirage = {}

        # Composantes générées au fur et à mesure
        self.chapeaux: List = []
        self.poules: Optional[dict] = None
        self.calendrier: Optional[List] = None
        self.phase_finale: Optional[dict] = None

    def creer_chapeaux(self) -> List[Chapeau]:
        """Crée les chapeaux du tournoi, du plus fort au plus faible."""
        nombre_chapeaux = math.ceil(len(self.joueurs) / 2)
        self.chapeaux = [Chapeau(i + 1) for i in range(nombre_chapeaux)]

        # Tri des joueurs par niveau (du plus fort au plus faible)
        joueurs_tries = sorted(self.joueurs, key=lambda j: j.niveau, reverse=True)

        nb_joueurs_par_chapeau = len(joueurs_tries) // nombre_chapeaux
        reste = len(joueurs_tries) % nombre_chapeaux

        index = 0
        for i, chapeau in enumerate(self.chapeaux):
            n = nb_joueurs_par_chapeau + (1 if i < reste else 0)
            for _ in range(n):
                chapeau.ajouter_joueur(joueurs_tries[index])
                index += 1

        return self.chapeaux

    def effectuer_tirage(self):
        """
        Effectue le tirage au sort à partir des chapeaux existants.
        et crée les poules en conséquence.
        
        Pour 8 joueurs : 2 poules de 4 (Pile et Face).
        Sinon : 1 poule unique avec tous les joueurs.
        """

        if not self.chapeaux:
            raise ValueError("Les chapeaux doivent être créés avant le tirage.")
        
        self.tirage = TirageService.tirer_au_sort(self.chapeaux)

        if self.nb_joueurs == 8:            
            self.poules = [
                Poule("Groupe Pile", [self.tirage[f"{i}p"] for i in range(1, len(self.chapeaux) + 1)]),
                Poule("Groupe Face", [self.tirage[f"{i}f"] for i in range(1, len(self.chapeaux) + 1)])
            ]
        else:
            self.poules = [Poule("Poule unique", self.joueurs)]

        return self.tirage
    
    def generer_matchs(self):
        """
        Génère les matchs pour chaque poule à partir du calendrier.
        - 8 joueurs : 2 poules de 6 matchs chacune.
        - Sinon : 1 poule unique avec tous les matchs.
        """
        if not self.poules:
            raise ValueError("Les poules doivent être créées avant de générer les matchs.")
        
        # Génération du calendrier complet à partir du tirage
        calendrier = CalendrierService.generer_calendrier(self.tirage)

        if self.nb_joueurs == 8:
            # 12 matchs : 6 pour Pile, 6 pour Face
            matchs_pile = calendrier[:6]
            matchs_face = calendrier[6:]

            # Attribution des matchs à chaque poule
            self.poules[0].matchs = [Match(j1, j2) for j1, j2 in matchs_pile]
            self.poules[1].matchs = [Match(j1, j2) for j1, j2 in matchs_face]
        else:
            # Un seul groupe → tous les matchs dans la même poule
            self.poules[0].matchs = [Match(j1, j2) for j1, j2 in calendrier]

    def generer_calendrier_phase_poule(self):
        """Génère le calendrier pour chaque poule de la phase de poule."""
        for poule in self.poules:
            if not poule.matchs:
                raise ValueError("Les matchs doivent être générés avant de créer le calendrier.")
            poule.generer_calendrier()
        self.calendrier = [poule.calendrier for poule in self.poules]

    def determiner_qualifies(self):
        if self.nb_joueurs == 6:
            return self.poules[0].qualifies(4)
        if self.nb_joueurs == 7:
            return self.poules[0].qualifies(7)
        if self.nb_joueurs == 8:
            return self.poules[0].qualifies(2) + self.poules[1].qualifies(2)
        raise ValueError(f"Nombre de joueurs non pris en charge : {self.nb_joueurs}")

    def lancer_phase_finale(self):
        participants = self.determiner_qualifies()

        if len(participants) == 4:
            self.demis = [
                MatchKO(participants[0], participants[3]),  # 1er vs 4ème dans le cas 6 joueurs, 1er groupe Pile vs 2ème groupe Face dans le cas 8 joueurs
                MatchKO(participants[1], participants[2])   # 2ème vs 3ème dans le cas 6 joueurs, 1er groupe Face vs 2ème groupe Pile dans le cas 8 joueurs
            ]
            self.finale = None

        elif len(participants) == 7:
            self.barrages = [
                MatchKO(participants[3], participants[4]),  # Dans cet ordre pour éviter de jouer barrage-demie à la suite
                MatchKO(participants[2], participants[5]),
                MatchKO(participants[1], participants[6])
            ]
            self.demis = None
            self.finale = None

        else:
            raise ValueError(f"Nombre de participants inattendu : {len(participants)}")

    def generer_demis_apres_barrages(self):
        premier_poule = self.determiner_qualifies()[0]

        vainqueurs_barrages = [m.vainqueur for m in self.barrages]
        if None in vainqueurs_barrages:
            raise ValueError("Tous les barrages doivent être joués avant de générer les demi-finales.")
        
        self.demis = [
            MatchKO(premier_poule, vainqueurs_barrages[0]),
            MatchKO(vainqueurs_barrages[2], vainqueurs_barrages[1])
        ]
        
    def generer_finale(self):
        if self.demis is None or any(df.vainqueur is None for df in self.demis):
            raise ValueError("Tous les demi-finales doivent être jouées avant de générer la finale.")
    
        vainqueurs_demis = [df.vainqueur for df in self.demis]
        self.finale = MatchKO(vainqueurs_demis[0], vainqueurs_demis[1])

    def __repr__(self):
        titre = ''
        if self.id ==1:
            titre = f'1er Tournoi {self.nom} ({self.date})'
        else:
            titre = f'{self.id}ème Tournoi {self.nom} ({self.date})'
        return titre