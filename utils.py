# =========================================================
# Fichier  : utils.py
# Projet   : Optimisation Production Laitière — EMSI
# Auteurs  : Aymane AIT ELMOUMEN, Rihab CHAROUQ,
#            Khalil LAKNIFLI, Ibrahim OURHANIM
# Encadré  : Badr DAKKAK & Yassine SAFSOUF
# Année    : 2025-2026
# =========================================================

"""
Fonctions utilitaires partagées pour l'affichage des tableaux,
titres formatés et vérifications des contraintes.
"""

from donnees import get_donnees


def afficher_titre(titre: str) -> None:
    """
    Affiche un titre encadré par des lignes de caractères '=' dans le terminal.
    
    Args:
        titre: Le texte du titre à afficher
    """
    largeur = 60
    print("\n" + "=" * largeur)
    print(f"  {titre}")
    print("=" * largeur)


def afficher_tableau(headers: list, rows: list, titre: str = "") -> None:
    """
    Affiche un tableau formaté en ASCII dans le terminal.
    Calcule automatiquement la largeur de chaque colonne.
    
    Args:
        headers: Liste des en-têtes de colonnes
        rows: Liste des lignes (chaque ligne est une liste de valeurs)
        titre: Titre optionnel du tableau
    """
    if titre:
        print(f"\n{titre}")
    
    # Convertir toutes les valeurs en chaînes
    str_headers = [str(h) for h in headers]
    str_rows = [[str(cell) for cell in row] for row in rows]
    
    # Calculer la largeur de chaque colonne
    col_widths = []
    for i in range(len(str_headers)):
        header_len = len(str_headers[i])
        max_data_len = max([len(row[i]) for row in str_rows], default=0)
        col_widths.append(max(header_len, max_data_len) + 2)
    
    # Ligne de séparation
    separator = "+" + "+".join(["-" * w for w in col_widths]) + "+"
    
    # Afficher le tableau
    print(separator)
    header_line = "|"
    for i, h in enumerate(str_headers):
        header_line += f" {h:^{col_widths[i]-2}} |"
    print(header_line)
    print(separator)
    
    for row in str_rows:
        row_line = "|"
        for i, cell in enumerate(row):
            row_line += f" {cell:^{col_widths[i]-2}} |"
        print(row_line)
    
    print(separator)


def afficher_verification(label: str, valeur: float, limite: float,
                          signe: str = "≤", unite: str = "") -> None:
    """
    Affiche une ligne de vérification de contrainte avec ✓ ou ✗
    et indication (saturée) si applicable.
    
    Args:
        label: Nom de la contrainte
        valeur: Valeur calculée
        limite: Limite de la contrainte
        signe: Symbole de comparaison (défaut: ≤)
        unite: Unité de mesure (ex: "kg", "L")
    """
    unite_str = f" {unite}" if unite else ""
    val_str = f"{valeur:.2f}" if isinstance(valeur, float) else str(valeur)
    lim_str = f"{limite:.2f}" if isinstance(limite, float) else str(limite)
    
    if valeur <= limite + 1e-9:  # Tolérance pour les erreurs de flottants
        symbole = "✓"
        saturée = " (contrainte SATURÉE)" if abs(valeur - limite) < 1e-6 else ""
        print(f"  {label:12s} : {val_str}{unite_str} {signe} {lim_str}{unite_str} {symbole}{saturée}")
    else:
        print(f"  {label:12s} : {val_str}{unite_str} {signe} {lim_str}{unite_str} ✗ (DÉPASSÉ)")


def afficher_donnees_probleme() -> None:
    """
    Affiche le tableau des données du problème (ressources et consommations par produit)
    ainsi que les justifications technologiques pour chaque produit.
    Utilise les données dynamiques configurées par l'utilisateur.
    """
    donnees = get_donnees()
    res = donnees.ressources
    
    afficher_titre("DONNÉES DU PROBLÈME — Entreprise Laitière")
    
    print(f"\n  Ressources disponibles par jour :")
    print(f"    • Lait cru           : {res.lait_disponible} litres/jour")
    print(f"    • Sucre              : {res.sucre_disponible} kg/jour")
    print(f"    • Ferments lactiques : {res.ferments_disponibles} kg/jour")
    
    print("\n  Un lot = 1 kg de produit fini (sauf P1 = 10 L)")
    
    # Tableau des produits
    headers = ["Produit", "Nom", "Lait L/lot", "Sucre kg/lot",
               "Ferments kg/lot", "Profit DH/lot", "Min lots"]
    rows = []
    for p in donnees.produits:
        min_str = f"{p.contrainte_min:.0f}" if p.contrainte_min > 0 else "—"
        rows.append([
            p.code, p.nom,
            f"{p.lait_par_lot:.1f}",
            f"{p.sucre_par_lot:.1f}",
            f"{p.ferments_par_lot:.1f}",
            f"{p.profit_par_lot:.0f}",
            min_str
        ])
    
    afficher_tableau(headers, rows, "\n  Tableau des produits et caractéristiques :")
