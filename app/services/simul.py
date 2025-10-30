import random

def simuler_match(match):
    """Simule un match, gère prolongations et TAB si phase finale."""
    score1 = random.randint(0, 4)
    score2 = random.randint(0, 3)

    # Phase finale (Barrage, Demi, Finale)
    if hasattr(match, "phase"):  
        if score1 == score2:
            # Prolongations
            prolong1 = random.randint(0, 2)
            prolong2 = random.randint(0, 2)
            # Tirs au but si égalité après prolong
            if prolong1 == prolong2:
                tab1 = random.randint(0, 5)
                tab2 = tab1 + 1  # assure un vainqueur
            else:
                tab1 = tab2 = None
            match.enregistrer_resultat(score1, score2, prolong1, prolong2, tab1, tab2)
        else:
            match.enregistrer_resultat(score1, score2)
    else:
        # Match classique / poule
        match.enregistrer_resultat(score1, score2)
