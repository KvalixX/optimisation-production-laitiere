# =========================================================
# Fichier  : chapitre1_graphique.py
# Projet   : Optimisation Production Laitière — EMSI
# Auteurs  : Aymane AIT ELMOUMEN, Rihab CHAROUQ,
#            Khalil LAKNIFLI, Ibrahim OURHANIM
# Encadré  : Badr DAKKAK & Yassine SAFSOUF
# Année    : 2025-2026
# =========================================================

"""
Chapitre 1 — Méthode Graphique (2 variables : x2 = Fromage, x3 = Yaourt)
Résolution complète avec tracé matplotlib et vérification scipy.
Version dynamique - les données sont configurables par l'utilisateur.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog
from utils import afficher_titre, afficher_tableau, afficher_verification
from donnees import get_donnees


def get_probleme_2var():
    """Récupère les données du problème à 2 variables (P2=Fromage, P3=Yaourt)."""
    donnees = get_donnees()
    res = donnees.ressources
    p2 = donnees.produits[1]  # Fromage
    p3 = donnees.produits[2]  # Yaourt
    
    # Contraintes simplifiées (divisées par 10 pour lait si nécessaire pour simplification)
    # Gardons les valeurs originales
    return {
        'ressources': res,
        'p2': p2,
        'p3': p3,
        # Coefficients des contraintes
        'a_lait_p2': p2.lait_par_lot,
        'a_lait_p3': p3.lait_par_lot,
        'a_sucre_p2': p2.sucre_par_lot,
        'a_sucre_p3': p3.sucre_par_lot,
        'a_ferm_p2': p2.ferments_par_lot,
        'a_ferm_p3': p3.ferments_par_lot,
        # Limites
        'lait_max': res.lait_disponible,
        'sucre_max': res.sucre_disponible,
        'ferm_max': res.ferments_disponibles,
        # Profits
        'c2': p2.profit_par_lot,
        'c3': p3.profit_par_lot
    }


def section0_entete():
    """Section 0 — En-tête et introduction."""
    data = get_probleme_2var()
    
    afficher_titre("CHAPITRE 1 — Problème à 2 Variables — Méthode Graphique")
    
    print("\n  Problématique :")
    print(f"    'Quelles quantités de {data['p2'].nom.lower()} et de {data['p3'].nom.lower()}")
    print("     produire quotidiennement afin de maximiser notre profit,")
    print("     sans dépasser nos stocks de matières premières ?'")
    
    print(f"\n  Les deux produits concernés :")
    print(f"    • P2 = {data['p2'].nom} (variable x₂)")
    print(f"    • P3 = {data['p3'].nom} (variable x₃)")


def section1_formulation():
    """Section 1 — Formulation mathématique avec données dynamiques."""
    data = get_probleme_2var()
    
    afficher_titre("SECTION 1 — Formulation Mathématique")
    
    print(f"\n  Variables de décision :")
    print(f"    x₂ = lots de {data['p2'].nom} produits par jour")
    print(f"    x₃ = lots de {data['p3'].nom} produits par jour")
    
    print(f"\n  Fonction objectif :")
    print(f"    max Z = {data['c2']:.0f}·x₂ + {data['c3']:.0f}·x₃")
    
    print(f"\n  Contraintes (avec noms) :")
    print(f"    Δ1 (Lait cru)   : {data['a_lait_p2']:.0f}·x₂ + {data['a_lait_p3']:.0f}·x₃ ≤ {data['lait_max']:.0f}")
    print(f"    Δ2 (Sucre)      : {data['a_sucre_p2']:.0f}·x₂ + {data['a_sucre_p3']:.0f}·x₃ ≤ {data['sucre_max']:.0f}")
    print(f"    Δ3 (Ferments)   : {data['a_ferm_p2']:.0f}·x₂ + {data['a_ferm_p3']:.0f}·x₃ ≤ {data['ferm_max']:.0f}")
    print(f"    Non-négativité  : x₂, x₃ ≥ 0")


def section2_droites_frontieres():
    """Section 2 — Tracé des droites frontières."""
    data = get_probleme_2var()
    afficher_titre("SECTION 2 — Tracé des Droites Frontières")
    
    # Calcul des intersections avec les axes
    # Δ1: a2*x2 + a3*x3 = Lait_max
    # Si x2=0: x3 = Lait_max / a3
    # Si x3=0: x2 = Lait_max / a2
    
    delta1_x3_0 = data['lait_max'] / data['a_lait_p3'] if data['a_lait_p3'] > 0 else float('inf')
    delta1_x2_0 = data['lait_max'] / data['a_lait_p2'] if data['a_lait_p2'] > 0 else float('inf')
    
    # Δ2: a_sucre_p2*x2 + a_sucre_p3*x3 = Sucre_max
    delta2_x3_0 = data['sucre_max'] / data['a_sucre_p3'] if data['a_sucre_p3'] > 0 else float('inf')
    
    # Δ3: a_ferm_p2*x2 + a_ferm_p3*x3 = Ferm_max
    delta3_x3_0 = data['ferm_max'] / data['a_ferm_p3'] if data['a_ferm_p3'] > 0 else float('inf')
    delta3_x2_0 = data['ferm_max'] / data['a_ferm_p2'] if data['a_ferm_p2'] > 0 else float('inf')
    
    headers = ["Droite", "Équation", "Si x₂ = 0", "Si x₃ = 0"]
    rows = [
        ["Δ1 (Lait)", f"{data['a_lait_p2']:.0f}·x₂ + {data['a_lait_p3']:.0f}·x₃ = {data['lait_max']:.0f}", 
         f"x₃ = {delta1_x3_0:.1f}" if delta1_x3_0 != float('inf') else "—", 
         f"x₂ = {delta1_x2_0:.1f}" if delta1_x2_0 != float('inf') else "—"],
        ["Δ2 (Sucre)", f"{data['a_sucre_p2']:.0f}·x₂ + {data['a_sucre_p3']:.0f}·x₃ = {data['sucre_max']:.0f}", 
         f"x₃ = {delta2_x3_0:.1f}" if delta2_x3_0 != float('inf') else "—", "—"],
        ["Δ3 (Ferm)", f"{data['a_ferm_p2']:.0f}·x₂ + {data['a_ferm_p3']:.0f}·x₃ = {data['ferm_max']:.0f}", 
         f"x₃ = {delta3_x3_0:.1f}" if delta3_x3_0 != float('inf') else "—", 
         f"x₂ = {delta3_x2_0:.1f}" if delta3_x2_0 != float('inf') else "—"]
    ]
    
    afficher_tableau(headers, rows, "\n  Tableau des intersections avec les axes :")


def calculer_sommets():
    """Calcule les sommets de la région réalisable dynamiquement."""
    data = get_probleme_2var()
    
    a_l2, a_l3 = data['a_lait_p2'], data['a_lait_p3']
    a_s2, a_s3 = data['a_sucre_p2'], data['a_sucre_p3']
    a_f2, a_f3 = data['a_ferm_p2'], data['a_ferm_p3']
    L, S, F = data['lait_max'], data['sucre_max'], data['ferm_max']
    c2, c3 = data['c2'], data['c3']
    
    # O(0, 0)
    sommets = [{'nom': 'O', 'x2': 0, 'x3': 0, 'Z': 0, 'contraintes': 'Axes', 'realisable': True}]
    
    # A: Intersection Δ1 avec x3=0 (si a_l2 > 0)
    if a_l2 > 0:
        x2_a = L / a_l2
        x3_a = 0
        Z_a = c2 * x2_a + c3 * x3_a
        # Vérifier si réalisable
        real_a = (a_s2 * x2_a + a_s3 * x3_a <= S + 1e-9) and (a_f2 * x2_a + a_f3 * x3_a <= F + 1e-9)
        sommets.append({'nom': 'A', 'x2': x2_a, 'x3': x3_a, 'Z': Z_a, 'contraintes': 'Δ1 ∩ {x₃=0}', 'realisable': real_a})
    
    # D: Intersection Δ2 avec Δ3 ou axe
    # Si x2=0: x3 = min(S/a_s3, F/a_f3) si les coeffs > 0
    candidats_x3 = []
    if a_s3 > 0:
        candidats_x3.append(S / a_s3)
    if a_f3 > 0:
        candidats_x3.append(F / a_f3)
    if candidats_x3:
        x3_d = min(candidats_x3)
        x2_d = 0
        Z_d = c2 * x2_d + c3 * x3_d
        real_d = (a_l2 * x2_d + a_l3 * x3_d <= L + 1e-9)
        sommets.append({'nom': 'D', 'x2': x2_d, 'x3': x3_d, 'Z': Z_d, 'contraintes': 'Δ2 ∩ Δ3', 'realisable': real_d})
    
    # Intersection Δ1 et Δ3
    # a_l2*x2 + a_l3*x3 = L
    # a_f2*x2 + a_f3*x3 = F
    det = a_l2 * a_f3 - a_l3 * a_f2
    if abs(det) > 1e-9:
        x2_b = (L * a_f3 - a_l3 * F) / det
        x3_b = (a_l2 * F - L * a_f2) / det
        if x2_b >= -1e-9 and x3_b >= -1e-9:
            Z_b = c2 * x2_b + c3 * x3_b
            # Vérifier contrainte sucre
            real_b = (a_s2 * x2_b + a_s3 * x3_b <= S + 1e-9)
            sommets.append({'nom': 'B', 'x2': x2_b, 'x3': x3_b, 'Z': Z_b, 'contraintes': 'Δ1 ∩ Δ3', 'realisable': real_b})
    
    # Intersection Δ1 et Δ2 (si a_s2 = 0)
    if a_s2 == 0 and a_s3 > 0:
        x3_int = S / a_s3
        if a_l3 > 0 and x3_int <= L / a_l3:
            x2_int = (L - a_l3 * x3_int) / a_l2 if a_l2 > 0 else 0
            Z_int = c2 * x2_int + c3 * x3_int
            real_int = (a_f2 * x2_int + a_f3 * x3_int <= F + 1e-9)
            if not real_int:
                sommets.append({'nom': 'C (rejeté)', 'x2': x2_int, 'x3': x3_int, 'Z': Z_int, 'contraintes': 'Δ1 ∩ Δ2', 'realisable': False})
    
    # Trouver le sommet optimal parmi les réalisables
    optimal = None
    max_Z = -float('inf')
    for s in sommets:
        if s['realisable'] and s['Z'] > max_Z:
            max_Z = s['Z']
            optimal = s
    
    if optimal:
        optimal['optimal'] = True
    
    return sommets, optimal


def section3_sommets():
    """Section 3 — Calcul des sommets de la région réalisable."""
    data = get_probleme_2var()
    sommets, optimal = calculer_sommets()
    
    afficher_titre("SECTION 3 — Calcul des Sommets de la Région Réalisable")
    
    for s in sommets:
        opt_marker = " — OPTIMAL" if s.get('optimal') else ""
        real_marker = "✓ RÉALISABLE" if s['realisable'] else "✗ NON RÉALISABLE"
        
        print(f"\n  Sommet {s['nom']}({s['x2']:.1f}, {s['x3']:.1f}){opt_marker}:")
        print(f"    → Contraintes actives : {s['contraintes']}")
        print(f"    → Z = {data['c2']:.0f}×{s['x2']:.1f} + {data['c3']:.0f}×{s['x3']:.1f} = {s['Z']:.0f} DH")
        print(f"    → {real_marker}")


def section4_tableau_sommets():
    """Section 4 — Tableau des sommets et évaluation de Z."""
    data = get_probleme_2var()
    sommets, optimal = calculer_sommets()
    
    afficher_titre("SECTION 4 — Tableau des Sommets et Évaluation de Z")
    
    headers = ["Sommet", "(x₂, x₃)", "Contraintes actives", f"Z = {data['c2']:.0f}x₂ + {data['c3']:.0f}x₃", "Optimal"]
    rows = []
    for s in sommets:
        opt_str = "✓" if s.get('optimal') else ""
        x2_str = f"{s['x2']:.1f}".rstrip('0').rstrip('.')
        x3_str = f"{s['x3']:.1f}".rstrip('0').rstrip('.')
        rows.append([
            s['nom'].replace(' (rejeté)', ''),
            f"({x2_str}, {x3_str})",
            s['contraintes'],
            f"{s['Z']:.0f} DH",
            opt_str
        ])
    
    afficher_tableau(headers, rows)


def section5_scipy():
    """Section 5 — Résolution avec scipy."""
    data = get_probleme_2var()
    
    afficher_titre("SECTION 5 — Résolution avec SciPy (linprog)")
    
    # Conversion en minimisation
    c = [-data['c2'], -data['c3']]
    A_ub = [
        [data['a_lait_p2'], data['a_lait_p3']],
        [data['a_sucre_p2'], data['a_sucre_p3']],
        [data['a_ferm_p2'], data['a_ferm_p3']]
    ]
    b_ub = [data['lait_max'], data['sucre_max'], data['ferm_max']]
    bounds = [(0, None), (0, None)]
    
    result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
    
    print("\n  Paramètres de résolution :")
    print("    • Méthode : 'highs'")
    print(f"    • Fonction objectif (min) : {-data['c2']:.0f}·x₂ {-data['c3']:.0f}·x₃")
    print("    • Contraintes : A_ub·x ≤ b_ub")
    
    print("\n  Résultat SciPy :")
    x2_opt = result.x[0]
    x3_opt = result.x[1]
    z_opt = data['c2'] * x2_opt + data['c3'] * x3_opt
    
    print(f"    • x₂ = {x2_opt:.2f} lots de {data['p2'].nom}")
    print(f"    • x₃ = {x3_opt:.2f} lots de {data['p3'].nom}")
    print(f"    • Z* = {z_opt:.2f} DH/jour")
    print(f"    • Statut : {result.message}")


def section6_verification():
    """Section 6 — Vérification des contraintes."""
    data = get_probleme_2var()
    sommets, optimal = calculer_sommets()
    
    afficher_titre("SECTION 6 — Vérification des Contraintes")
    
    if optimal is None:
        print("\n  ⚠ Aucune solution optimale trouvée.")
        return
    
    x2, x3 = optimal['x2'], optimal['x3']
    
    print(f"\n  Solution optimale : x₂ = {x2:.1f}, x₃ = {x3:.1f}\n")
    
    # Calculs
    lait = data['a_lait_p2'] * x2 + data['a_lait_p3'] * x3
    sucre = data['a_sucre_p2'] * x2 + data['a_sucre_p3'] * x3
    ferments = data['a_ferm_p2'] * x2 + data['a_ferm_p3'] * x3
    
    print("  Vérification détaillée :")
    afficher_verification("Lait cru", lait, data['lait_max'], "≤", "L")
    print(f"    Calcul : {data['a_lait_p2']:.0f}×{x2:.1f} + {data['a_lait_p3']:.0f}×{x3:.1f} = {lait:.1f} L")
    
    afficher_verification("Sucre", sucre, data['sucre_max'], "≤", "kg")
    print(f"    Calcul : {data['a_sucre_p2']:.0f}×{x2:.1f} + {data['a_sucre_p3']:.0f}×{x3:.1f} = {sucre:.1f} kg")
    exc_sucre = data['sucre_max'] - sucre
    if exc_sucre > 1:
        print(f"    Excédent : {data['sucre_max']:.0f} - {sucre:.1f} = {exc_sucre:.1f} kg/jour disponible")
    
    afficher_verification("Ferments", ferments, data['ferm_max'], "≤", "kg")
    print(f"    Calcul : {data['a_ferm_p2']:.0f}×{x2:.1f} + {data['a_ferm_p3']:.0f}×{x3:.1f} = {ferments:.1f} kg")
    
    print("\n  Solution optimale finale :")
    headers = ["Variable", "Prod", "Quantité", "Unité", "Profit partiel (DH)"]
    profit_x2 = data['c2'] * x2
    profit_x3 = data['c3'] * x3
    rows = [
        ["x₂", data['p2'].nom[:4] + ".", f"{x2:.1f} lots", f"{x2:.1f} kg", f"{data['c2']:.0f} × {x2:.1f} = {profit_x2:,.0f}".replace(",", " ")],
        ["x₃", data['p3'].nom[:4] + ".", f"{x3:.1f} lots", f"{x3:.1f} kg", f"{data['c3']:.0f} × {x3:.1f} = {profit_x3:,.0f}".replace(",", " ")]
    ]
    afficher_tableau(headers, rows)
    print(f"\n    Profit total journalier Z* = {optimal['Z']:.0f} DH")


def section7_interpretation():
    """Section 7 — Interprétation économique."""
    data = get_probleme_2var()
    sommets, optimal = calculer_sommets()
    
    afficher_titre("SECTION 7 — Interprétation Économique")
    
    if optimal is None:
        print("\n  ⚠ Aucune solution optimale trouvée.")
        return
    
    x2, x3 = optimal['x2'], optimal['x3']
    
    # Calcul des consommations
    lait = data['a_lait_p2'] * x2 + data['a_lait_p3'] * x3
    sucre = data['a_sucre_p2'] * x2 + data['a_sucre_p3'] * x3
    ferments = data['a_ferm_p2'] * x2 + data['a_ferm_p3'] * x3
    
    # Ressources saturées
    saturées = []
    if abs(lait - data['lait_max']) < 1:
        saturées.append("lait cru")
    if abs(sucre - data['sucre_max']) < 1:
        saturées.append("sucre")
    if abs(ferments - data['ferm_max']) < 1:
        saturées.append("ferments lactiques")
    
    print(f"\n  1. Plan de production optimal :")
    print(f"     Produire simultanément x₂={x2:.1f} lots de {data['p2'].nom.lower()} et x₃={x3:.1f} lots")
    print(f"     de {data['p3'].nom.lower()} par jour.")
    
    print(f"\n  2. Ressources saturées :")
    if saturées:
        sat_str = " et ".join(saturées)
        print(f"     Le {sat_str} sont entièrement consommés → goulots d'étranglement.")
    else:
        print("     Aucune ressource saturée.")
    
    print(f"\n  3. Ressources disponibles :")
    exc_lait = data['lait_max'] - lait
    exc_sucre = data['sucre_max'] - sucre
    exc_ferm = data['ferm_max'] - ferments
    if exc_lait > 1:
        print(f"     Lait: excédent de {exc_lait:.1f} L/jour")
    if exc_sucre > 1:
        print(f"     Sucre: excédent de {exc_sucre:.1f} kg/jour")
    if exc_ferm > 1:
        print(f"     Ferments: excédent de {exc_ferm:.1f} kg/jour")
    
    print(f"\n  4. Conseil stratégique :")
    if saturées:
        print(f"     Pour augmenter le profit, augmenter l'approvisionnement")
        print(f"     en { ' et en '.join(saturées) } (contraintes actives).")
    else:
        print("     Analyse complémentaire nécessaire pour les recommandations.")


def section8_graphique():
    """Section 8 — Graphique matplotlib dynamique."""
    data = get_probleme_2var()
    sommets_list, optimal = calculer_sommets()
    
    afficher_titre("SECTION 8 — Graphique Matplotlib (sauvegarde PNG)")
    
    print("\n  Création du graphique...")
    
    fig, ax = plt.subplots(figsize=(10, 7), dpi=100)
    
    # Filtrer les sommets réalisables uniquement pour le polygone
    sommets_realisables = [(s['x2'], s['x3']) for s in sommets_list if s['realisable']]
    
    # Trier les sommets pour former un polygone correct (ordre des angles)
    if len(sommets_realisables) >= 3:
        # Centroid pour le tri angulaire
        cx = sum(x for x, y in sommets_realisables) / len(sommets_realisables)
        cy = sum(y for x, y in sommets_realisables) / len(sommets_realisables)
        sommets_realisables.sort(key=lambda p: np.arctan2(p[1] - cy, p[0] - cx))
    
    # Tracé des droites contraintes
    # Calcul des limites pour l'axe
    max_x = max([s['x2'] for s in sommets_list] + [50]) * 1.5
    max_y = max([s['x3'] for s in sommets_list] + [200]) * 1.2
    x2 = np.linspace(0, max_x, 100)
    
    # Δ1 (Lait cru)
    if data['a_lait_p3'] > 0:
        x3_delta1 = (data['lait_max'] - data['a_lait_p2'] * x2) / data['a_lait_p3']
        ax.plot(x2, x3_delta1, 'r-', linewidth=2, 
                label=f"Δ1 (Lait) : {data['a_lait_p2']:.0f}x₂ + {data['a_lait_p3']:.0f}x₃ ≤ {data['lait_max']:.0f}")
    
    # Δ2 (Sucre)
    if data['a_sucre_p3'] > 0:
        x3_delta2 = (data['sucre_max'] - data['a_sucre_p2'] * x2) / data['a_sucre_p3']
        ax.plot(x2, x3_delta2, 'b--', linewidth=2, 
                label=f"Δ2 (Sucre) : {data['a_sucre_p2']:.0f}x₂ + {data['a_sucre_p3']:.0f}x₃ ≤ {data['sucre_max']:.0f}")
    elif data['a_sucre_p2'] == 0 and data['a_sucre_p3'] > 0:
        ax.axhline(y=data['sucre_max'] / data['a_sucre_p3'], color='b', linestyle='--', linewidth=2,
                  label=f"Δ2 (Sucre) : x₃ ≤ {data['sucre_max'] / data['a_sucre_p3']:.0f}")
    
    # Δ3 (Ferments)
    if data['a_ferm_p3'] > 0:
        x3_delta3 = (data['ferm_max'] - data['a_ferm_p2'] * x2) / data['a_ferm_p3']
        ax.plot(x2, x3_delta3, 'g-.', linewidth=2, 
                label=f"Δ3 (Ferm) : {data['a_ferm_p2']:.0f}x₂ + {data['a_ferm_p3']:.0f}x₃ ≤ {data['ferm_max']:.0f}")
    
    # Remplissage de la région réalisable
    if len(sommets_realisables) >= 3:
        # Fermer le polygone
        poly_x = [s[0] for s in sommets_realisables] + [sommets_realisables[0][0]]
        poly_y = [s[1] for s in sommets_realisables] + [sommets_realisables[0][1]]
        ax.fill(poly_x, poly_y, color='lightgreen', alpha=0.3, label='Région réalisable')
    
    # Droite de niveau Z optimal (si optimal existe)
    if optimal:
        x3_z = (optimal['Z'] - data['c2'] * x2) / data['c3'] if data['c3'] > 0 else np.zeros_like(x2)
        ax.plot(x2, x3_z, color='gold', linestyle=':', linewidth=1.5, 
                label=f"Z* = {optimal['Z']:.0f} DH (optimal)")
    
    # Points des sommets
    for s in sommets_list:
        sx, sy = s['x2'], s['x3']
        is_opt = s.get('optimal', False)
        
        if is_opt:
            ax.plot(sx, sy, marker='*', markersize=20, color='gold', markeredgecolor='black',
                   markeredgewidth=1, zorder=5)
        else:
            color = 'red' if s['realisable'] else 'gray'
            ax.plot(sx, sy, marker='o', markersize=8, color=color, zorder=5)
        
        # Label
        offset_x = max_x * 0.03 if sx < max_x * 0.7 else -max_x * 0.15
        offset_y = max_y * 0.03 if sy < max_y * 0.6 else -max_y * 0.08
        label = f"{s['nom']}({sx:.1f},{sy:.1f})"
        if is_opt:
            label += " ★"
        ax.annotate(label, (sx + offset_x, sy + offset_y), fontsize=9,
                   fontweight='bold' if is_opt else 'normal')
    
    # Configuration des axes
    ax.set_xlim(0, max_x)
    ax.set_ylim(0, max_y)
    ax.set_xlabel(f"x₂ — {data['p2'].nom} (lots)", fontsize=11)
    ax.set_ylabel(f"x₃ — {data['p3'].nom} (lots)", fontsize=11)
    ax.set_title('Région réalisable et solution optimale\nMéthode graphique (x₂, x₃)',
                fontsize=13, fontweight='bold')
    ax.grid(True, linestyle='-', alpha=0.3)
    ax.legend(loc='upper right', fontsize=8)
    
    # Sauvegarde
    plt.tight_layout()
    plt.savefig('chapitre1_region_realisable.png', dpi=100, bbox_inches='tight')
    print("  ✓ Graphique sauvegardé : 'chapitre1_region_realisable.png'")
    
    plt.show()


def run_chapitre1():
    """
    Fonction principale qui exécute toutes les sections du chapitre 1
    dans l'ordre, avec des pauses d'affichage claires.
    """
    section0_entete()
    section1_formulation()
    section2_droites_frontieres()
    section3_sommets()
    section4_tableau_sommets()
    section5_scipy()
    section6_verification()
    section7_interpretation()
    section8_graphique()
    
    print("\n" + "=" * 60)
    print("  Fin du Chapitre 1 — Méthode Graphique")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    run_chapitre1()
