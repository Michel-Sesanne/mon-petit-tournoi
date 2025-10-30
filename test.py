from app.models import Tournoi, Joueur
from app.services import simul

def test():
    # --- Exemple de création d'un tournoi ---
    joueurs = [
        Joueur("Alex", 8),
        Joueur("J.F", 7),
        Joueur("Michel", 6),
        Joueur("Yves", 5),
        Joueur("Etienne", 4),
        Joueur("Julien", 3),
        Joueur("Flo", 2),
        Joueur("Fabien", 1)
    ]

    tournoi = Tournoi(3, "FC25", "18-10-2025", joueurs)
    print(tournoi)
    print('')

    # --- Création des chapeaux ---
    chapeaux = tournoi.creer_chapeaux()
    for chapeau in chapeaux:
        print(f"Chapeau {chapeau.numero}: {[joueur.nom for joueur in chapeau.joueurs]}")
    print('')

    # --- Tirage au sort ---
    print(tournoi.effectuer_tirage())
    print('')

    # --- Génération du calendrier de la phase de poule ---
    tournoi.generer_matchs()
    tournoi.generer_calendrier_phase_poule()

    for i, poule in enumerate(tournoi.poules):
        print(f"--- Poule {i+1} ---")
        for match in tournoi.calendrier[i].matchs:
            simul.simuler_match(match)  # simule le score
        print(tournoi.calendrier[i])
        print(poule)
        print('')

    # --- Lancer la phase finale ---
    tournoi.lancer_phase_finale()

    # --- Barrages si présents (ex: 7 joueurs) ---
    if hasattr(tournoi, 'barrages') and tournoi.barrages:
        print("--- Barrages ---")
        for match in tournoi.barrages:
            simul.simuler_match(match)
            print(match)
        tournoi.generer_demis_apres_barrages()
        print('')

    # --- Demi-finales ---
    print("--- Demi-finales ---")
    for match in tournoi.demis:
        simul.simuler_match(match)
        print(match)
    print('')

    # --- Finale ---
    tournoi.generer_finale()
    print("--- Finale ---")
    finale = tournoi.finale
    simul.simuler_match(finale)
    print(finale)
    print('')
    print("🏆 Vainqueur du tournoi :", finale.vainqueur)



    

