# =========================================================
# Fichier  : main.py
# Projet   : Optimisation Production Laitière — EMSI
# Auteurs  : Aymane AIT ELMOUMEN, Rihab CHAROUQ,
#            Khalil LAKNIFLI, Ibrahim OURHANIM
# Encadré  : Badr DAKKAK & Yassine SAFSOUF
# Année    : 2025-2026
# =========================================================

"""
Menu principal interactif pour le projet d'optimisation de la production
d'une entreprise laitière par programmation linéaire.

Options disponibles :
    [1] Chapitre 1 — Méthode Graphique (2 variables)
    [2] Chapitre 2 — Méthode du Simplexe (4 variables)
    [3] Exécuter les deux chapitres complets
    [4] Afficher les données du problème
    [5] Configurer les données du problème (personnalisation)
    [6] Réinitialiser aux données par défaut
    [0] Quitter
"""

import sys
from chapitre1_graphique import run_chapitre1
from chapitre2_simplexe import run_chapitre2
from utils import afficher_donnees_probleme
from donnees import saisir_donnees_interactif, reinitialiser_donnees, get_donnees


def afficher_menu():
    """Affiche le menu principal en ASCII art."""
    donnees = get_donnees()
    mode_str = "(CONFIGURÉ)" if donnees != None else ""
    
    print("\n" + "=" * 70)
    print("║" + " " * 68 + "║")
    print("║     OPTIMISATION DE LA PRODUCTION D'UNE ENTREPRISE LAITIÈRE        ║")
    print("║     Programmation Linéaire & Python — EMSI 3ème IIR                ║")
    print("║" + " " * 68 + "║")
    print("=" * 70)
    print("║  Réalisé par : Aymane AIT ELMOUMEN  |  Rihab CHAROUQ               ║")
    print("║               Khalil LAKNIFLI       |  Ibrahim OURHANIM            ║")
    print("║  Encadré par : Badr DAKKAK & Yassine SAFSOUF                       ║")
    print("║  Année Universitaire 2025-2026                                      ║")
    print("=" * 70)
    print("║                                                                     ║")
    print("║  [1] Chapitre 1 — Méthode Graphique        (2 variables)           ║")
    print("║  [2] Chapitre 2 — Méthode du Simplexe      (4 variables)           ║")
    print("║  [3] Exécuter les deux chapitres complets                            ║")
    print("║  [4] Afficher les données du problème                              ║")
    print("║  [5] Configurer les données (variables dynamiques)   ★             ║")
    print("║  [6] Réinitialiser aux données par défaut                            ║")
    print("║  [0] Quitter                                                         ║")
    print("║" + " " * 68 + "║")
    print("=" * 70)


def main():
    """Fonction principale — boucle interactive du menu."""
    while True:
        afficher_menu()
        choix = input("\n  Votre choix : ").strip()
        
        if choix == "1":
            print("\n  → Lancement du Chapitre 1 : Méthode Graphique...")
            run_chapitre1()
            
        elif choix == "2":
            print("\n  → Lancement du Chapitre 2 : Méthode du Simplexe...")
            run_chapitre2()
            
        elif choix == "3":
            print("\n  → Exécution des deux chapitres complets...")
            print("\n" + "=" * 70)
            print("  PREMIÈRE PARTIE : CHAPITRE 1 — MÉTHODE GRAPHIQUE")
            print("=" * 70)
            run_chapitre1()
            
            print("\n" + "=" * 70)
            print("  DEUXIÈME PARTIE : CHAPITRE 2 — MÉTHODE DU SIMPLEXE")
            print("=" * 70)
            run_chapitre2()
            
        elif choix == "4":
            print("\n  → Affichage des données du problème...")
            afficher_donnees_probleme()
            
        elif choix == "5":
            print("\n  → Configuration des données du problème...")
            saisir_donnees_interactif()
            
        elif choix == "6":
            print("\n  → Réinitialisation des données...")
            reinitialiser_donnees()
            
        elif choix == "0":
            print("\n  Au revoir ! Merci d'avoir utilisé notre programme.\n")
            sys.exit(0)
            
        else:
            print("\n  ⚠ Choix invalide, veuillez réessayer.")
        
        # Pause avant de réafficher le menu
        input("\n  Appuyez sur Entrée pour continuer...")


if __name__ == "__main__":
    # Vérifier les dépendances au démarrage
    try:
        import numpy
        import matplotlib
        import scipy
    except ImportError as e:
        print("\n" + "=" * 60)
        print("  ERREUR : Dépendances manquantes")
        print("=" * 60)
        print(f"\n  {e}")
        print("\n  Veuillez installer les dépendances requises :")
        print("    pip install -r requirements.txt")
        print("\n  Ou :")
        print("    pip install numpy matplotlib scipy")
        sys.exit(1)
    
    main()
