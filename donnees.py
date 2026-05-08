# =========================================================
# Fichier  : donnees.py
# Projet   : Optimisation Production Laitière — EMSI
# Auteurs  : Aymane AIT ELMOUMEN, Rihab CHAROUQ,
#            Khalil LAKNIFLI, Ibrahim OURHANIM
# Encadré  : Badr DAKKAK & Yassine SAFSOUF
# Année    : 2025-2026
# =========================================================

"""
Module de gestion des données dynamiques du problème d'optimisation.
Permet à l'utilisateur de saisir ses propres valeurs ou d'utiliser les valeurs par défaut.
"""

from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class Produit:
    """Représente un produit laitier avec ses caractéristiques."""
    code: str
    nom: str
    lait_par_lot: float
    sucre_par_lot: float
    ferments_par_lot: float
    profit_par_lot: float
    contrainte_min: float = 0


@dataclass
class Ressources:
    """Représente les ressources disponibles."""
    lait_disponible: float
    sucre_disponible: float
    ferments_disponibles: float


@dataclass
class DonneesProbleme:
    """Contient toutes les données du problème d'optimisation."""
    ressources: Ressources
    produits: List[Produit]


# Valeurs par défaut (original)
DONNEES_DEFAUT = DonneesProbleme(
    ressources=Ressources(
        lait_disponible=2200,
        sucre_disponible=300,
        ferments_disponibles=150
    ),
    produits=[
        Produit("P1", "Lait pasteurisé", 10, 0, 0, 20, contrainte_min=2),
        Produit("P2", "Fromage", 100, 0, 3, 500, contrainte_min=0),
        Produit("P3", "Yaourt", 10, 2, 1, 80, contrainte_min=10),
        Produit("P4", "Beurre", 200, 0, 0, 800, contrainte_min=1)
    ]
)

# Instance globale modifiable
donnees_actuelles = None


def get_donnees() -> DonneesProbleme:
    """Retourne les données actuelles (par défaut si non initialisées)."""
    global donnees_actuelles
    if donnees_actuelles is None:
        donnees_actuelles = DONNEES_DEFAUT
    return donnees_actuelles


def set_donnees(donnees: DonneesProbleme):
    """Définit les données actuelles."""
    global donnees_actuelles
    donnees_actuelles = donnees


def saisir_float(prompt: str, valeur_defaut: float) -> float:
    """Saisit un nombre flottant avec valeur par défaut."""
    while True:
        try:
            valeur = input(f"{prompt} [{valeur_defaut}]: ").strip()
            if valeur == "":
                return valeur_defaut
            return float(valeur)
        except ValueError:
            print("  ⚠ Veuillez entrer un nombre valide.")


def saisir_donnees_interactif() -> DonneesProbleme:
    """Interface interactive de saisie des données du problème."""
    print("\n" + "=" * 60)
    print("  CONFIGURATION DES DONNÉES DU PROBLÈME")
    print("=" * 60)
    print("\n  (Appuyez sur Entrée pour garder la valeur par défaut)")
    
    # Saisie des ressources
    print("\n  --- RESSOURCES DISPONIBLES PAR JOUR ---")
    lait = saisir_float("  Lait cru (litres)", DONNEES_DEFAUT.ressources.lait_disponible)
    sucre = saisir_float("  Sucre (kg)", DONNEES_DEFAUT.ressources.sucre_disponible)
    ferments = saisir_float("  Ferments lactiques (kg)", DONNEES_DEFAUT.ressources.ferments_disponibles)
    
    ressources = Ressources(lait, sucre, ferments)
    
    # Saisie des produits
    print("\n  --- CARACTÉRISTIQUES DES PRODUITS ---")
    print("  Pour chaque produit, entrez les consommations par lot et le profit.\n")
    
    produits = []
    for prod_defaut in DONNEES_DEFAUT.produits:
        print(f"  Produit {prod_defaut.code} - {prod_defaut.nom}")
        
        lait_p_lot = saisir_float(f"    Lait (L/lot)", prod_defaut.lait_par_lot)
        sucre_p_lot = saisir_float(f"    Sucre (kg/lot)", prod_defaut.sucre_par_lot)
        ferments_p_lot = saisir_float(f"    Ferments (kg/lot)", prod_defaut.ferments_par_lot)
        profit = saisir_float(f"    Profit (DH/lot)", prod_defaut.profit_par_lot)
        min_prod = saisir_float(f"    Production minimale (lots)", prod_defaut.contrainte_min)
        
        produits.append(Produit(
            prod_defaut.code,
            prod_defaut.nom,
            lait_p_lot,
            sucre_p_lot,
            ferments_p_lot,
            profit,
            min_prod
        ))
        print()
    
    donnees = DonneesProbleme(ressources, produits)
    set_donnees(donnees)
    
    # Affichage récapitulatif
    afficher_donnees_saisies(donnees)
    
    return donnees


def afficher_donnees_saisies(donnees: DonneesProbleme):
    """Affiche un récapitulatif des données saisies."""
    print("\n" + "=" * 60)
    print("  RÉCAPITULATIF DES DONNÉES CONFIGURÉES")
    print("=" * 60)
    
    print(f"\n  Ressources disponibles:")
    print(f"    • Lait cru: {donnees.ressources.lait_disponible} L/jour")
    print(f"    • Sucre: {donnees.ressources.sucre_disponible} kg/jour")
    print(f"    • Ferments: {donnees.ressources.ferments_disponibles} kg/jour")
    
    print(f"\n  Produits:")
    headers = ["Code", "Nom", "Lait", "Sucre", "Ferm.", "Profit", "Min"]
    print(f"    {' | '.join([f'{h:^10}' for h in headers])}")
    print("    " + "-" * 75)
    
    for p in donnees.produits:
        vals = [
            f"{p.code:^10}",
            f"{p.nom[:10]:^10}",
            f"{p.lait_par_lot:^10.1f}",
            f"{p.sucre_par_lot:^10.1f}",
            f"{p.ferments_par_lot:^10.1f}",
            f"{p.profit_par_lot:^10.0f}",
            f"{p.contrainte_min:^10.0f}"
        ]
        print(f"    {' | '.join(vals)}")
    
    print("=" * 60)


def reinitialiser_donnees():
    """Réinitialise les données aux valeurs par défaut."""
    global donnees_actuelles
    donnees_actuelles = DONNEES_DEFAUT
    print("\n  ✓ Données réinitialisées aux valeurs par défaut.")
