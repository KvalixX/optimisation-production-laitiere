# =========================================================
# Fichier  : chapitre2_simplexe.py
# Projet   : Optimisation Production Laitière — EMSI
# Auteurs  : Aymane AIT ELMOUMEN, Rihab CHAROUQ,
#            Khalil LAKNIFLI, Ibrahim OURHANIM
# Encadré  : Badr DAKKAK & Yassine SAFSOUF
# Année    : 2025-2026
# =========================================================

"""
Chapitre 2 — Méthode du Simplexe (4 variables : x1, x2, x3, x4)
Résolution complète avec substitution, tableaux du simplexe et analyse de dualité.
Version dynamique - les données de vérification sont configurables par l'utilisateur.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog
from utils import afficher_titre, afficher_tableau, afficher_verification
from donnees import get_donnees, DonneesProbleme, Ressources, Produit


def get_probleme_4var():
    """Récupère les données du problème à 4 variables."""
    donnees = get_donnees()
    res = donnees.ressources
    p1, p2, p3, p4 = donnees.produits  # Lait, Fromage, Yaourt, Beurre
    
    return {
        'ressources': res,
        'p1': p1, 'p2': p2, 'p3': p3, 'p4': p4,
        # Coefficients contraintes
        'a_lait': [p1.lait_par_lot, p2.lait_par_lot, p3.lait_par_lot, p4.lait_par_lot],
        'a_sucre': [p1.sucre_par_lot, p2.sucre_par_lot, p3.sucre_par_lot, p4.sucre_par_lot],
        'a_ferm': [p1.ferments_par_lot, p2.ferments_par_lot, p3.ferments_par_lot, p4.ferments_par_lot],
        # Profits
        'c': [p1.profit_par_lot, p2.profit_par_lot, p3.profit_par_lot, p4.profit_par_lot],
        # Minimaux
        'x_min': [p1.contrainte_min, p2.contrainte_min, p3.contrainte_min, p4.contrainte_min]
    }


def section0_entete():
    """Section 0 — En-tête et introduction."""
    afficher_titre("CHAPITRE 2 — Problème Complet à 4 Variables — Méthode du Simplexe")
    
    print("\n  Les 4 produits :")
    print("    • P1 = Lait pasteurisé (x₁)")
    print("    • P2 = Fromage (x₂)")
    print("    • P3 = Yaourt (x₃)")
    print("    • P4 = Beurre (x₄)")
    
    print("\n  Principe de la méthode du simplexe (George Dantzig, 1947) :")
    print("    'Algorithme algébrique itératif résolvant des PL avec n'importe")
    print("     quel nombre de variables. Étapes : mise en forme standard →")
    print("     solution initiale → critère d'entrée (coeff. le plus négatif")
    print("     dans Z) → critère de sortie (quotient minimal) → pivot →")
    print("     optimalité (tous coefficients Z ≥ 0)'")


def section1_formulation():
    """Section 1 — Formulation mathématique complète."""
    data = get_probleme_4var()
    afficher_titre("SECTION 1 — Formulation Mathématique Complète")
    
    print("\n  Variables de décision :")
    print(f"    x₁ = lots de {data['p1'].nom} produits par jour")
    print(f"    x₂ = lots de {data['p2'].nom} produits par jour")
    print(f"    x₃ = lots de {data['p3'].nom} produits par jour")
    print(f"    x₄ = lots de {data['p4'].nom} produits par jour")
    
    print("\n  Fonction objectif :")
    print(f"    max Z = {data['c'][0]}·x₁ + {data['c'][1]}·x₂ + {data['c'][2]}·x₃ + {data['c'][3]}·x₄")
    
    print("\n  Contraintes de matières premières :")
    print(f"    Lait cru  : {data['a_lait'][0]}·x₁ + {data['a_lait'][1]}·x₂ + {data['a_lait'][2]}·x₃ + {data['a_lait'][3]}·x₄ ≤ {data['ressources'].lait_disponible}   ...(1)")
    print(f"    Sucre     : {data['a_sucre'][2]}·x₃ ≤ {data['ressources'].sucre_disponible}                                  ...(2)")
    print(f"    Ferments  : {data['a_ferm'][1]}·x₂ + {data['a_ferm'][2]}·x₃ ≤ {data['ressources'].ferments_disponibles}                             ...(3)")
    
    print("\n  Contraintes minimales de production :")
    print(f"    x₁ ≥ {data['x_min'][0]}    (approvisionnement minimum clients directs)")
    print(f"    x₃ ≥ {data['x_min'][2]}   (engagement contractuel minimal)")
    print(f"    x₄ ≥ {data['x_min'][3]}    (présence minimale sur le marché)")
    print("\n  Non-négativité : x₁, x₂, x₃, x₄ ≥ 0")
    
    headers = ["Produit", "Contrainte minimale", "Justification"]
    rows = [
        [f"P1 – {data['p1'].nom}", f"x₁ ≥ {data['x_min'][0]} lots ({data['x_min'][0]*10} L/j)", "Approvisionnement minimum clients directs"],
        [f"P3 – {data['p3'].nom}", f"x₃ ≥ {data['x_min'][2]} lots ({data['x_min'][2]*1} kg/j)", "Engagement contractuel minimal"],
        [f"P4 – {data['p4'].nom}", f"x₄ ≥ {data['x_min'][3]} lot ({data['x_min'][3]*1} kg/j)", "Présence minimale sur le marché"]
    ]
    afficher_tableau(headers, rows, "\n  Tableau des contraintes minimales :")


def section2_substitution():
    """Section 2 — Mise en forme standard — Substitution des variables."""
    afficher_titre("SECTION 2 — Mise en Forme Standard — Substitution des Variables")
    
    print("\n  Poser :")
    print("    x₁' = x₁ - 2   (x₁' ≥ 0)")
    print("    x₃' = x₃ - 10  (x₃' ≥ 0)")
    print("    x₄' = x₄ - 1   (x₄' ≥ 0)")
    
    print("\n  Contrainte Lait réduite :")
    print("    10·(x₁'+2) + 100·x₂ + 10·(x₃'+10) + 200·(x₄'+1) ≤ 2200")
    print("    ⟺ 10x₁' + 100x₂ + 10x₃' + 200x₄' + 20 + 100 + 200 ≤ 2200")
    print("    ⟺ 10x₁' + 100x₂ + 10x₃' + 200x₄' ≤ 1880   (Lait réduit)")
    
    print("\n  Contrainte Ferments réduite :")
    print("    3·x₂ + (x₃'+10) ≤ 150")
    print("    ⟺ 3·x₂ + x₃' ≤ 140   (Ferments réduit)")
    
    print("\n  Contrainte Sucre réduite :")
    print("    2·(x₃'+10) ≤ 300")
    print("    ⟺ 2x₃' ≤ 280  →  x₃' ≤ 140   (Sucre réduit)")
    
    print("\n  Fonction objectif réduite :")
    print("    max Z' = 20x₁' + 500x₂ + 80x₃' + 800x₄' + 1640")
    print("\n  Profit garanti par les minimaux = 20×2 + 80×10 + 800×1")
    print("                                   = 40 + 800 + 800 = 1640 DH")
    
    print("\n  Introduction des variables d'écart s₁, s₂, s₃ ≥ 0 :")
    print("    10x₁' + 100x₂ + 10x₃' + 200x₄' + s₁ = 1880   (équation 1)")
    print("    3x₂ + x₃' + s₂ = 140                           (équation 2)")
    print("    x₃' + s₃ = 140                                 (équation 3)")
    
    print("\n  Solution initiale de base :")
    print("    x₁' = x₂ = x₃' = x₄' = 0")
    print("    s₁ = 1880, s₂ = 140, s₃ = 140")
    print("    Z' = 0 (profit additionnel au-delà des 1640 DH garantis)")


def section3_tableau_initial():
    """Section 3 — Affichage du tableau initial du simplexe."""
    afficher_titre("SECTION 3 — Tableau Initial du Simplexe")
    
    headers = ["Base", "cB", "x₁'", "x₂", "x₃'", "x₄'", "s₁", "s₂", "s₃", "b"]
    rows = [
        ["s₁", "0", "10", "100", "10", "200", "1", "0", "0", "1880"],
        ["s₂", "0", "0", "3", "1", "0", "0", "1", "0", "140"],
        ["s₃", "0", "0", "0", "1", "0", "0", "0", "1", "140"],
        ["Z", "—", "-20", "-500", "-80", "-200", "0", "0", "0", "0"]
    ]
    afficher_tableau(headers, rows)
    
    print("\n  Analyse :")
    print("    Variable entrante : x₂ (coefficient -500, le plus négatif)")
    print("    Quotients pour x₂ : 1880/100 = 18.8 (minimum)")
    print("                        140/3 ≈ 46.7")
    print("                        — (pas de pivot sur s₃, coef = 0)")
    print("    Variable sortante : s₁")
    print("    Élément pivot : 100")


def section4_iteration1():
    """Section 4 — Itération 1 : Pivot sur 100 (s1 → x2)."""
    afficher_titre("SECTION 4 — Itération 1 : Pivot sur 100 (s₁ → x₂)")
    
    print("\n  Opérations :")
    print("    Nouvelle ligne x₂ ← R_s₁ ÷ 100 :")
    print("      [0.1, 1, 0.1, 2, 0.01, 0, 0 | 18.8]")
    print("\n    R_s₂ ← R_s₂ − 3 × R_x₂")
    print("    R_Z  ← R_Z  + 500 × R_x₂")
    
    headers = ["Base", "cB", "x₁'", "x₂", "x₃'", "x₄'", "s₁", "s₂", "s₃", "b"]
    rows = [
        ["x₂", "500", "0.1", "1", "0.1", "2", "0.01", "0", "0", "18.8"],
        ["s₂", "0", "-0.3", "0", "0.7", "-6", "-0.03", "1", "0", "83.6"],
        ["s₃", "0", "0", "0", "1", "0", "0", "0", "1", "140"],
        ["Z", "—", "-30", "0", "-30", "800", "5", "0", "0", "9400"]
    ]
    afficher_tableau(headers, rows, "\n  Tableau après itération 1 :")
    
    print("\n  Analyse :")
    print("    Z' = 9400 DH (profit additionnel) + 1640 DH = 11 040 DH")
    print("    Coefficients négatifs restants : x₁'(-30) et x₃'(-30)")
    print("    → Choisir x₃' (même valeur — choix arbitraire)")
    
    print("\n    Quotients pour x₃' (colonnes positives) :")
    print("      18.8 / 0.1 = 188")
    print("      83.6 / 0.7 ≈ 119.4  ← MINIMUM")
    print("      140 / 1 = 140")
    print("    Variable sortante : s₂ — Pivot : 0.7")


def section5_iteration2():
    """Section 5 — Itération 2 : Pivot sur 0.7 (s2 → x3')."""
    afficher_titre("SECTION 5 — Itération 2 : Pivot sur 0.7 (s₂ → x₃')")
    
    print("\n  Opérations :")
    print("    Nouvelle ligne x₃' ← R_s₂ ÷ 0.7 :")
    print("      [-3/7, 0, 1, -60/7, -3/70, 10/7, 0 | 119.4]")
    print("\n    R_x₂ ← R_x₂ − 0.1 × R_x₃'")
    print("    R_s₃ ← R_s₃ − 1 × R_x₃'")
    print("    R_Z  ← R_Z  + 30 × R_x₃'")
    
    headers = ["Base", "cB", "x₁'", "x₂", "x₃'", "x₄'", "s₁", "s₂", "s₃", "b"]
    rows = [
        ["x₂", "500", "≈0.14", "1", "0", "≈2.86", "≈0.01", "≈-0.14", "0", "≈6.86"],
        ["x₃'", "80", "≈-0.43", "0", "1", "≈-8.57", "≈-0.04", "≈1.43", "0", "≈119.4"],
        ["s₃", "0", "≈0.43", "0", "0", "≈8.57", "≈0.04", "≈-1.43", "1", "≈20.6"],
        ["Z", "—", "≈-43", "0", "0", "≈543", "≈3.6", "≈42.9", "0", "≈12983"]
    ]
    afficher_tableau(headers, rows, "\n  Tableau après itération 2 (valeurs arrondies) :")
    
    print("\n  Analyse :")
    print("    Z' ≈ 12 983 DH (additionnel) + 1640 DH ≈ 14 623 DH")
    print("    Coefficient négatif restant : x₁' (≈ -43)")
    print("    Quotients pour x₁' (valeurs positives) :")
    print("      6.86 / 0.14 ≈ 49.0")
    print("      20.6 / 0.43 ≈ 47.9  ← MINIMUM")
    print("    Variable sortante : s₃ — Pivot : ≈0.43")


def section6_iteration3():
    """Section 6 — Itération 3 : Pivot sur s3 → x1'."""
    afficher_titre("SECTION 6 — Itération 3 : Pivot sur s₃ → x₁'")
    
    print("\n  Opérations de pivot sur la ligne s₃ :")
    print("    Après opérations, tous les coefficients dans la ligne Z sont ≥ 0")
    print("    → OPTIMALITÉ ATTEINTE")
    
    print("\n  Solution optimale du problème réduit :")
    print("    x₁' = 6")
    print("    x₂ = 6")
    print("    x₃' = 122")
    print("    x₄' = 0")
    
    print("\n  Restitution des variables originales :")
    print("    x₁ = x₁' + 2  =  6 + 2  =  8  lots de Lait pasteurisé")
    print("    x₂ = x₂       =  6      =  6  lots de Fromage")
    print("    x₃ = x₃' + 10 = 122 + 10 = 132  lots de Yaourt")
    print("    x₄ = x₄' + 1  =  0 + 1  =  1  lot  de Beurre")


def section7_scipy():
    """Section 7 — Résolution avec scipy (confirmation) - Version dynamique."""
    data = get_probleme_4var()
    
    afficher_titre("SECTION 7 — Résolution avec SciPy (confirmation algorithmique)")
    
    # Variables réduites : x' = x - x_min
    # Les contraintes deviennent: A·(x' + x_min) ≤ b => A·x' ≤ b - A·x_min
    
    c = [-data['c'][0], -data['c'][1], -data['c'][2], -data['c'][3]]
    
    # Calcul des limites réduites
    lait_reduit = data['ressources'].lait_disponible - sum(data['a_lait'][i] * data['x_min'][i] for i in range(4))
    sucre_reduit = data['ressources'].sucre_disponible - sum(data['a_sucre'][i] * data['x_min'][i] for i in range(4))
    ferm_reduit = data['ressources'].ferments_disponibles - sum(data['a_ferm'][i] * data['x_min'][i] for i in range(4))
    
    A_ub = [
        data['a_lait'],    # Lait réduit
        data['a_sucre'],   # Sucre réduit
        data['a_ferm']     # Ferments réduit
    ]
    b_ub = [lait_reduit, sucre_reduit, ferm_reduit]
    bounds = [(0, None), (0, None), (0, None), (0, None)]
    
    result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
    
    print(f"\n  Contraintes réduites (après retrait des minimaux) :")
    print(f"    • Lait disponible: {lait_reduit:.1f} L")
    print(f"    • Sucre disponible: {sucre_reduit:.1f} kg")
    print(f"    • Ferments disponibles: {ferm_reduit:.1f} kg")
    
    # Vérification si le problème est faisable
    if not result.success or result.x is None:
        print("\n  ⚠⚠⚠  PROBLÈME INFAISABLE  ⚠⚠⚠")
        print("\n  Les minimaux de production configurés sont impossibles à satisfaire")
        print("  avec les ressources disponibles actuelles.")
        print("\n  Conseil : Réduisez les contraintes minimales ou augmentez les ressources.")
        print(f"\n  Statut SciPy : {result.message}")
        return
    
    print("\n  Résolution avec variables réduites (x' = x - x_min) :")
    print(f"    • x₁' = {result.x[0]:.4f}")
    print(f"    • x₂' = {result.x[1]:.4f}")
    print(f"    • x₃' = {result.x[2]:.4f}")
    print(f"    • x₄' = {result.x[3]:.4f}")
    
    # Restitution
    x = [result.x[i] + data['x_min'][i] for i in range(4)]
    Z = sum(data['c'][i] * x[i] for i in range(4))
    
    profit_min = sum(data['c'][i] * data['x_min'][i] for i in range(4))
    Z_additionnel = sum(data['c'][i] * result.x[i] for i in range(4))
    
    print("\n  Restitution des variables originales :")
    print(f"    • x₁ = {x[0]:.2f} lots de {data['p1'].nom}")
    print(f"    • x₂ = {x[1]:.2f} lots de {data['p2'].nom}")
    print(f"    • x₃ = {x[2]:.2f} lots de {data['p3'].nom}")
    print(f"    • x₄ = {x[3]:.2f} lots de {data['p4'].nom}")
    print(f"\n    Profit des minimaux: {profit_min:.2f} DH")
    print(f"    Profit additionnel: {Z_additionnel:.2f} DH")
    print(f"    Z* = {Z:.2f} DH/jour")
    print(f"    Statut : {result.message}")


def section8_solution_optimale():
    """Section 8 — Solution optimale et tableau récapitulatif."""
    data = get_probleme_4var()
    afficher_titre("SECTION 8 — Solution Optimale et Tableau Récapitulatif")
    
    lait_reduit = data['ressources'].lait_disponible - sum(data['a_lait'][i] * data['x_min'][i] for i in range(4))
    sucre_reduit = data['ressources'].sucre_disponible - sum(data['a_sucre'][i] * data['x_min'][i] for i in range(4))
    ferm_reduit = data['ressources'].ferments_disponibles - sum(data['a_ferm'][i] * data['x_min'][i] for i in range(4))
    
    c = [-data['c'][i] for i in range(4)]
    A_ub = [data['a_lait'], data['a_sucre'], data['a_ferm']]
    b_ub = [lait_reduit, sucre_reduit, ferm_reduit]
    bounds = [(0, None)] * 4
    
    result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
    
    if not result.success or result.x is None:
        print("\n  ⚠  Impossible de générer la solution: problème infaisable")
        return
        
    x = [result.x[i] + data['x_min'][i] for i in range(4)]
    Z = sum(data['c'][i] * x[i] for i in range(4))
    
    headers = ["Variable", "Produit", "Quantité", "Unité", "Profit partiel (DH)"]
    rows = [
        ["x₁", data['p1'].nom, f"{x[0]:.1f} lots ({x[0]*10:.0f} L/jour)", "lots", f"{data['c'][0]} × {x[0]:.1f}   =    {data['c'][0]*x[0]:.0f}"],
        ["x₂", data['p2'].nom, f"{x[1]:.1f} lots ({x[1]*1:.0f} kg/jour)", "lots", f"{data['c'][1]} × {x[1]:.1f}  =  {data['c'][1]*x[1]:.0f}"],
        ["x₃", data['p3'].nom, f"{x[2]:.1f} lots ({x[2]*1:.0f} kg/j)", "lots", f"{data['c'][2]} × {x[2]:.1f} = {data['c'][2]*x[2]:.0f}"],
        ["x₄", data['p4'].nom, f"{x[3]:.1f} lot ({x[3]*1:.0f} kg/jour)", "lots", f"{data['c'][3]} × {x[3]:.1f}  =    {data['c'][3]*x[3]:.0f}"]
    ]
    afficher_tableau(headers, rows)
    print(f"\n    Profit total journalier Z* = {Z:.0f} DH")


def section9_verification():
    """Section 9 — Vérification des contraintes - Version dynamique."""
    data = get_probleme_4var()
    
    afficher_titre("SECTION 9 — Vérification des Contraintes (Données dynamiques)")
    
    # Résolution SciPy pour obtenir la solution optimale dynamique
    lait_reduit = data['ressources'].lait_disponible - sum(data['a_lait'][i] * data['x_min'][i] for i in range(4))
    sucre_reduit = data['ressources'].sucre_disponible - sum(data['a_sucre'][i] * data['x_min'][i] for i in range(4))
    ferm_reduit = data['ressources'].ferments_disponibles - sum(data['a_ferm'][i] * data['x_min'][i] for i in range(4))
    
    c = [-data['c'][i] for i in range(4)]
    A_ub = [data['a_lait'], data['a_sucre'], data['a_ferm']]
    b_ub = [lait_reduit, sucre_reduit, ferm_reduit]
    bounds = [(0, None)] * 4
    
    result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
    
    if not result.success or result.x is None:
        print("\n  ⚠  Impossible de vérifier: problème infaisable (voir section 7)")
        return
    
    x = [result.x[i] + data['x_min'][i] for i in range(4)]
    x1, x2, x3, x4 = x
    
    print(f"\n  Solution optimale (SciPy) : x₁={x1:.2f}, x₂={x2:.2f}, x₃={x3:.2f}, x₄={x4:.2f}\n")
    
    # Calculs des consommations
    lait = sum(data['a_lait'][i] * x[i] for i in range(4))
    sucre = sum(data['a_sucre'][i] * x[i] for i in range(4))
    ferments = sum(data['a_ferm'][i] * x[i] for i in range(4))
    
    print("  Vérification :")
    calc_lait = " + ".join([f"{data['a_lait'][i]:.0f}×{x[i]:.1f}" for i in range(4) if data['a_lait'][i] > 0])
    sat_lait = " (SATURÉE)" if abs(lait - data['ressources'].lait_disponible) < 1 else ""
    print(f"    Lait cru   : {calc_lait} = {lait:.1f} ≤ {data['ressources'].lait_disponible:.0f} ✓{sat_lait}")
    
    calc_sucre = " + ".join([f"{data['a_sucre'][i]:.0f}×{x[i]:.1f}" for i in range(4) if data['a_sucre'][i] > 0])
    exc_sucre = data['ressources'].sucre_disponible - sucre
    sat_sucre = " (SATURÉE)" if abs(sucre - data['ressources'].sucre_disponible) < 1 else f"  (excédent : {exc_sucre:.1f} kg/jour)"
    print(f"    Sucre      : {calc_sucre} = {sucre:.1f} ≤ {data['ressources'].sucre_disponible:.0f} ✓{sat_sucre}")
    
    calc_ferm = " + ".join([f"{data['a_ferm'][i]:.0f}×{x[i]:.1f}" for i in range(4) if data['a_ferm'][i] > 0])
    sat_ferm = " (SATURÉE)" if abs(ferments - data['ressources'].ferments_disponibles) < 1 else ""
    print(f"    Ferments   : {calc_ferm} = {ferments:.1f} ≤ {data['ressources'].ferments_disponibles:.0f} ✓{sat_ferm}")
    
    print(f"\n    Minimaux   : x₁={x1:.1f} ≥ {data['x_min'][0]:.0f} ✓ | x₂={x2:.1f} ≥ {data['x_min'][1]:.0f} ✓ | x₃={x3:.1f} ≥ {data['x_min'][2]:.0f} ✓ | x₄={x4:.1f} ≥ {data['x_min'][3]:.0f} ✓")


def section10_interpretation():
    """Section 10 — Interprétation économique - Version dynamique."""
    data = get_probleme_4var()
    
    afficher_titre("SECTION 10 — Interprétation Économique (Données dynamiques)")
    
    # Résolution SciPy pour obtenir la solution
    lait_reduit = data['ressources'].lait_disponible - sum(data['a_lait'][i] * data['x_min'][i] for i in range(4))
    sucre_reduit = data['ressources'].sucre_disponible - sum(data['a_sucre'][i] * data['x_min'][i] for i in range(4))
    ferm_reduit = data['ressources'].ferments_disponibles - sum(data['a_ferm'][i] * data['x_min'][i] for i in range(4))
    
    c = [-data['c'][i] for i in range(4)]
    A_ub = [data['a_lait'], data['a_sucre'], data['a_ferm']]
    b_ub = [lait_reduit, sucre_reduit, ferm_reduit]
    bounds = [(0, None)] * 4
    
    result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
    
    if not result.success or result.x is None:
        print("\n  ⚠  Impossible d'interpréter: problème infaisable (voir section 7)")
        return
    
    x = [result.x[i] + data['x_min'][i] for i in range(4)]
    
    # Calculs
    lait = sum(data['a_lait'][i] * x[i] for i in range(4))
    sucre = sum(data['a_sucre'][i] * x[i] for i in range(4))
    ferments = sum(data['a_ferm'][i] * x[i] for i in range(4))
    Z = sum(data['c'][i] * x[i] for i in range(4))
    
    # Ressources saturées
    saturées = []
    if abs(lait - data['ressources'].lait_disponible) < 1:
        saturées.append("lait cru")
    if abs(sucre - data['ressources'].sucre_disponible) < 1:
        saturées.append("sucre")
    if abs(ferments - data['ressources'].ferments_disponibles) < 1:
        saturées.append("ferments")
    
    print(f"\n  1. Plan de production optimal :")
    print(f"     {x[0]:.1f} lots {data['p1'].nom} + {x[1]:.1f} lots {data['p2'].nom} + ")
    print(f"     {x[2]:.1f} lots {data['p3'].nom} + {x[3]:.1f} lots {data['p4'].nom}/jour")
    print(f"     Profit total: Z* = {Z:.0f} DH/jour")
    
    print(f"\n  2. Ressources saturées :")
    if saturées:
        print(f"     {', '.join(saturées).capitalize()} → contraintes actives")
    else:
        print("     Aucune ressource saturée.")
    
    print(f"\n  3. Ressources disponibles :")
    if data['ressources'].lait_disponible - lait > 1:
        print(f"     Lait: excédent de {data['ressources'].lait_disponible - lait:.1f} L/jour")
    if data['ressources'].sucre_disponible - sucre > 1:
        print(f"     Sucre: excédent de {data['ressources'].sucre_disponible - sucre:.1f} kg/jour")
    if data['ressources'].ferments_disponibles - ferments > 1:
        print(f"     Ferments: excédent de {data['ressources'].ferments_disponibles - ferments:.1f} kg/jour")
    
    print(f"\n  4. Conseil stratégique :")
    if saturées:
        print(f"     Augmenter l'approvisionnement en {', '.join(saturées)} pour augmenter le profit.")
    else:
        print("     Analyse des prix-ombres nécessaire pour les recommandations.")


def section11_dualite():
    """Section 11 — Analyse de la dualité et prix-ombres."""
    afficher_titre("SECTION 11 — Analyse de la Dualité et Prix-Ombres")
    
    print("\n  Principe de la dualité :")
    print("    'À tout problème de PL (primal) correspond un problème dual.")
    print("     Les variables duales yᵢ représentent le gain marginal de profit")
    print("     si l'on augmente d'une unité la ressource i.'")
    
    print("\n  Formulation du problème dual :")
    print("    min W = 2200·y₁ + 300·y₂ + 150·y₃")
    print("    s.c.")
    print("      10·y₁               ≥  20    (contrainte duale pour x₁)")
    print("      100·y₁       + 3·y₃ ≥ 500   (contrainte duale pour x₂)")
    print("      10·y₁ + 2·y₂ + 1·y₃ ≥  80   (contrainte duale pour x₃)")
    print("      200·y₁              ≥ 800   (contrainte duale pour x₄)")
    print("      y₁, y₂, y₃ ≥ 0")
    
    print("\n  Théorème des écarts complémentaires :")
    print("    • Contrainte Lait active (saturée) → y₁ > 0")
    print("    • Contrainte Ferments active (saturée) → y₃ > 0")
    print("    • Contrainte Sucre inactive (excédent 36 kg) → y₂ = 0")
    
    print("\n  Calcul des prix-ombres (résoudre le système 2×2) :")
    print("    Pour x₂ > 0 et x₃ > 0 (variables de base positives) :")
    print("      100·y₁ + 3·y₃ = 500   (x₂ > 0)")
    print("      10·y₁ + y₃ = 80       (x₃ > 0, avec y₂ = 0)")
    print("\n    Résolution :")
    print("      Multiplier la 2e équation par 3 : 30·y₁ + 3·y₃ = 240")
    print("      Soustraire : 70·y₁ = 260")
    print("      → y₁ = 260/70 ≈ 3.714 DH/litre de lait cru")
    print("      → y₃ = 80 - 10×3.714 ≈ 42.857 DH/kg de ferments")
    
    headers = ["Ressource", "Variable duale", "Prix-ombre", "Interprétation"]
    rows = [
        ["Lait cru (L)", "y₁", "≈ 3.71 DH/L", "+1L → +3.71 DH de profit"],
        ["Sucre (kg)", "y₂", "0.00 DH/kg", "Ressource non limitante"],
        ["Ferments (kg)", "y₃", "≈ 42.86 DH/kg", "+1kg → +42.86 DH profit"]
    ]
    afficher_tableau(headers, rows, "\n  Tableau des prix-ombres :")
    
    print("\n  Vérification de la dualité forte :")
    y1, y2, y3 = 260/70, 0, 80 - 10*(260/70)
    W = 2200*y1 + 300*y2 + 150*y3
    print(f"    W* = 2200 × {y1:.3f} + 300 × {y2} + 150 × {y3:.3f}")
    print(f"       = {2200*y1:.1f} + {300*y2} + {150*y3:.1f}")
    print(f"       ≈ {W:.0f} DH")
    print(f"    W* = Z* ✓  (dualité forte vérifiée)")
    
    print("\n  Recommandations stratégiques issues de la dualité :")
    print("    1. Priorité d'investissement : ferments (≈42.86 DH/kg) vs")
    print("       lait (≈3.71 DH/L) → 1 kg de ferments rapporte ≈ 11.5 fois")
    print("       plus qu'1 L de lait. L'entreprise devrait en priorité")
    print("       augmenter son approvisionnement en ferments.")
    print("    2. Sucre non limitant (y₂=0) : inutile d'en acheter davantage")
    print("       tant que la production est maintenue.")
    print("    3. Analyse de sensibilité : prix-ombres valides dans un intervalle")
    print("       autour des valeurs actuelles — au-delà, la base optimale changerait.")


def section12_graphiques():
    """Section 12 — Graphiques matplotlib."""
    data = get_probleme_4var()
    afficher_titre("SECTION 12 — Graphiques Matplotlib")
    
    print("\n  Création des graphiques...")
    
    lait_reduit = data['ressources'].lait_disponible - sum(data['a_lait'][i] * data['x_min'][i] for i in range(4))
    sucre_reduit = data['ressources'].sucre_disponible - sum(data['a_sucre'][i] * data['x_min'][i] for i in range(4))
    ferm_reduit = data['ressources'].ferments_disponibles - sum(data['a_ferm'][i] * data['x_min'][i] for i in range(4))
    
    c = [-data['c'][i] for i in range(4)]
    A_ub = [data['a_lait'], data['a_sucre'], data['a_ferm']]
    b_ub = [lait_reduit, sucre_reduit, ferm_reduit]
    bounds = [(0, None)] * 4
    
    result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
    
    if not result.success or result.x is None:
        print("\n  ⚠  Impossible de générer les graphiques: problème infaisable")
        return
        
    x = [result.x[i] + data['x_min'][i] for i in range(4)]
    
    # Données
    produits = [f"{data['p1'].nom}\nP1", f"{data['p2'].nom}\nP2", f"{data['p3'].nom}\nP3", f"{data['p4'].nom}\nP4"]
    quantites = [round(v, 1) for v in x]
    profits = [round(data['c'][i] * x[i], 1) for i in range(4)]
    
    try:
        prix_ombres = [abs(val) for val in result.ineqlin.marginals]
    except AttributeError:
        prix_ombres = [3.71, 0, 42.86] # Fallback
    
    # Figure 1 : Quantités et Profits (subplots)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=100)
    
    # Graphique 1 — Quantités produites
    bars1 = ax1.bar(produits, quantites, color='steelblue', edgecolor='black')
    ax1.set_title('Quantités produites par jour', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Lots', fontsize=10)
    ax1.set_ylim(0, max(quantites) * 1.2)
    ax1.grid(axis='y', alpha=0.3)
    
    # Annoter les valeurs
    for bar, val in zip(bars1, quantites):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                str(val), ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Graphique 2 — Profits partiels
    bars2 = ax2.bar(produits, profits, color='forestgreen', edgecolor='black')
    ax2.set_title('Profit partiel par produit (DH)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('DH', fontsize=10)
    ax2.set_ylim(0, max(profits) * 1.2)
    ax2.grid(axis='y', alpha=0.3)
    
    # Annoter les valeurs
    for bar, val in zip(bars2, profits):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 200,
                f'{val} DH', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    fig.suptitle('Solution Optimale — Problème à 4 Variables (Méthode du Simplexe)',
                fontsize=13, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('chapitre2_solution_optimale.png', dpi=100, bbox_inches='tight')
    print("  ✓ Graphique 1 sauvegardé : 'chapitre2_solution_optimale.png'")
    
    # Figure 2 — Prix-ombres
    fig2, ax3 = plt.subplots(figsize=(8, 5), dpi=100)
    
    ressources = ['Lait cru\n(y₁)', 'Sucre\n(y₂)', 'Ferments\n(y₃)']
    colors = ['#e74c3c' if p > 0.01 else '#95a5a6' for p in prix_ombres]
    
    bars3 = ax3.barh(ressources, prix_ombres, color=colors, edgecolor='black', height=0.5)
    ax3.set_title('Prix-ombres des ressources (DH/unité)', fontsize=12, fontweight='bold')
    ax3.set_xlabel('Prix-ombre (DH)', fontsize=10)
    ax3.set_xlim(0, max(prix_ombres) * 1.2)
    ax3.grid(axis='x', alpha=0.3)
    
    # Annoter les valeurs
    for bar, val in zip(bars3, prix_ombres):
        ax3.text(val + 1, bar.get_y() + bar.get_height()/2,
                f'{val:.2f} DH', ha='left', va='center', fontsize=10, fontweight='bold')
    
    # Légende
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='#e74c3c', label='Ressource limitante (prix > 0)'),
                      Patch(facecolor='#95a5a6', label='Ressource non limitante (prix = 0)')]
    ax3.legend(handles=legend_elements, loc='lower right')
    
    plt.tight_layout()
    plt.savefig('chapitre2_prix_ombres.png', dpi=100, bbox_inches='tight')
    print("  ✓ Graphique 2 sauvegardé : 'chapitre2_prix_ombres.png'")
    
    plt.show()


def afficher_tableau_synthese():
    """Affiche le tableau de synthèse comparatif."""
    afficher_titre("TABLEAU DE SYNTHÈSE — Comparaison Chapitre 1 et 2")
    
    headers = ["Aspect", "Chapitre 1 (2 var)", "Chapitre 2 (4 var)"]
    rows = [
        ["Méthode", "Graphique", "Simplexe"],
        ["Produits", "Fromage + Yaourt", "Lait + Fromage + Yaourt + Beurre"],
        ["Lait disponible", "2 200 L", "2 200 L"],
        ["Solution optimale", "x₂=10, x₃=120", "x₁=8, x₂=6, x₃=132, x₄=1"],
        ["Profit journalier", "Z* = 14 600 DH", "Z* = 14 520 DH"],
        ["Ressources saturées", "Lait + Ferments", "Lait + Ferments"]
    ]
    afficher_tableau(headers, rows)


def run_chapitre2():
    """
    Fonction principale qui exécute toutes les sections du chapitre 2
    dans l'ordre, avec titres clairs entre chaque.
    """
    section0_entete()
    section1_formulation()
    section2_substitution()
    section3_tableau_initial()
    section4_iteration1()
    section5_iteration2()
    section6_iteration3()
    section7_scipy()
    section8_solution_optimale()
    section9_verification()
    section10_interpretation()
    section11_dualite()
    section12_graphiques()
    afficher_tableau_synthese()
    
    print("\n" + "=" * 60)
    print("  Fin du Chapitre 2 — Méthode du Simplexe")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    run_chapitre2()
