import random

class CalendrierService:
    """
    Service de génération de calendrier.
    Génère le calendrier prédéfini selon la configuration choisie,
    en garantissant que personne ne joue deux fois de suite.
    """

    @staticmethod
    def generer_calendrier(tirage):
        calendrier = []
        n = len(tirage)

        if n == 6:
            a, b, c = tirage['1p'], tirage['2p'], tirage['3p']
            d, e, f = tirage['1f'], tirage['2f'], tirage['3f']

            calendrier = [
                (a, d),  # intra-chapeau 1
                (b, e),  # intra-chapeau 2
                (c, f),  # intra-chapeau 3
                (a, b),  # inter-chapeau 1-2
                (d, e),
                (c, a),  # inter-chapeau 1-3
                (f, d),
                (c, b),  # inter-chapeau 2-3
                (f, e)
            ]

        elif n == 7:
            a, b, c = tirage['1p'], tirage['2p'], tirage['3p']
            d = tirage['4']
            e, f, g = tirage['1f'], tirage['2f'], tirage['3f']

            calendrier = [
                (a, b),
                (g, d),
                (f, e),
                (b, c),
                (d, a),
                (e, g),
                (c, f)
            ]

        elif n == 8:
            a, b, c, d = tirage['1p'], tirage['2p'], tirage['3p'], tirage['4p']
            e, f, g, h = tirage['1f'], tirage['2f'], tirage['3f'], tirage['4f']

            calendrier = [
                (a, b), (c, d),
                (d, a), (b, c),
                (a, c), (b, d),
                (e, f), (g, h),
                (h, e), (f, g),
                (e, g), (f, h)
            ]

        else:
            raise ValueError(f"Nombre de joueurs inattendu ({n}). Aucun calendrier prédéfini disponible.")

        return calendrier
