# Optimisation de la Production Laitière 🥛

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![EMSI](https://img.shields.io/badge/EMSI-3%C3%A8me_IIR-red.svg)

Ce projet est une application Python interactive d'optimisation de la production d'une entreprise laitière en utilisant la **Programmation Linéaire**. Il a été développé dans le cadre d'un projet universitaire à l'EMSI.

## 👥 Équipe du Projet

- **Auteurs :**
  - Aymane AIT ELMOUMEN
  - Rihab CHAROUQ
  - Khalil LAKNIFLI
  - Ibrahim OURHANIM
- **Encadré par :** Badr DAKKAK & Yassine SAFSOUF
- **Année Universitaire :** 2025-2026

## 🚀 Fonctionnalités

Le programme propose deux interfaces (une graphique et une en ligne de commande) permettant de :
- **Interface Graphique (Nouveau) :** Application de bureau conviviale (`gui.py`) avec console intégrée et formulaires interactifs pour la configuration des données.
- **Chapitre 1 — Méthode Graphique (2 variables) :** Résolution d'un sous-problème simplifié avec une visualisation graphique de la zone réalisable et de la droite de profit maximum (Isoprofit).
- **Chapitre 2 — Méthode du Simplexe (4 variables) :** Résolution du problème complet utilisant l'algorithme du simplexe, avec détail des itérations et tableaux intermédiaires.
- **Exécution combinée :** Lancement des deux chapitres successivement.
- **Affichage des données :** Consultation des paramètres actuels (profits, contraintes de production).
- **Configuration dynamique :** Saisie interactive de vos propres paramètres (profits par produit, limites de production, capacités, etc.) pour résoudre des cas pratiques variés.
- **Réinitialisation :** Retour rapide aux données par défaut du rapport d'étude.

## 🛠️ Installation et Prérequis

Assurez-vous d'avoir [Python 3.8+](https://www.python.org/) installé sur votre machine.

1. **Cloner le dépôt :**
   ```bash
   git clone https://github.com/KvalixX/optimisation-production-laitiere.git
   cd optimisation-production-laitiere
   ```

2. **Installer les dépendances requises :**
   Le projet s'appuie sur `numpy`, `matplotlib` et `scipy`.
   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Utilisation

Vous avez le choix entre deux interfaces pour utiliser l'application :

**Option 1 : Interface Graphique (Recommandée)**
Pour lancer l'application avec une interface visuelle conviviale (Tkinter), exécutez :
```bash
python gui.py
```

**Option 2 : Interface en Ligne de Commande**
Pour utiliser le menu interactif classique dans le terminal :
```bash
python main.py
```

Laissez-vous ensuite guider par les menus de l'interface choisie !

## 📂 Structure du Projet

- `gui.py` : Interface graphique de bureau (GUI) utilisant Tkinter.
- `main.py` : Point d'entrée de l'application et menu principal en ligne de commande.
- `chapitre1_graphique.py` : Logique mathématique et affichage matplotlib pour la méthode graphique.
- `chapitre2_simplexe.py` : Logique de l'algorithme du simplexe et affichage des tableaux pas-à-pas.
- `donnees.py` : Module de gestion (sauvegarde, modification, chargement) des variables de production.
- `utils.py` : Fonctions utilitaires, notamment pour le formatage des impressions console.
- `requirements.txt` : Fichier listant les dépendances Python nécessaires.

## 📜 Licence

Projet réalisé dans un cadre académique pour l'École Marocaine des Sciences de l'Ingénieur (EMSI).
