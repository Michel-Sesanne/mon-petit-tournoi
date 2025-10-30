import random
class TirageService:
    @staticmethod
    def tirer_au_sort(chapeaux):
        """
        Tirage pile/face pour tous les chapeaux ayant 2 joueurs,
        et joueur unique pour les chapeaux à 1 joueur.
        Retourne un dictionnaire avec les clés :
        '1p', '1f', '2p', '2f', ... ou '4' si un seul joueur.
        """
        
        tirages = {}
        for i, chapeau in enumerate(chapeaux, start=1):
            nb_joueurs = len(chapeau.joueurs)
            joueurs = chapeau.joueurs[:]
            random.shuffle(joueurs)

            if nb_joueurs == 2:
                tirages[f"{i}p"], tirages[f"{i}f"] = joueurs
            elif nb_joueurs == 1:
                tirages[f"{i}"] = joueurs[0]
            else:
                raise ValueError(f"Chapeau {i} a un nombre de joueurs inattendu : {nb_joueurs}")
        return tirages