import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sys
import threading
import matplotlib.pyplot as plt

# Imports du projet
from chapitre1_graphique import run_chapitre1
from chapitre2_simplexe import run_chapitre2
from utils import afficher_donnees_probleme
from donnees import reinitialiser_donnees, get_donnees, set_donnees, DonneesProbleme, Ressources, Produit, DONNEES_DEFAUT

class RedirectText:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.configure(state='normal')
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)
        self.text_widget.configure(state='disabled')

    def flush(self):
        pass


class ConfigDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Configuration des Données")
        self.geometry("600x650")
        self.transient(parent)
        self.grab_set()

        self.donnees = get_donnees()
        self.entries = {}

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas pour le scroll
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- RESSOURCES ---
        ttk.Label(scrollable_frame, text="RESSOURCES DISPONIBLES PAR JOUR", font=('Helvetica', 12, 'bold')).pack(pady=(10, 5), anchor='w')
        
        res_frame = ttk.LabelFrame(scrollable_frame, text="Ressources")
        res_frame.pack(fill="x", padx=5, pady=5)

        self.add_entry(res_frame, "Lait cru (L)", self.donnees.ressources.lait_disponible, "res_lait")
        self.add_entry(res_frame, "Sucre (kg)", self.donnees.ressources.sucre_disponible, "res_sucre")
        self.add_entry(res_frame, "Ferments (kg)", self.donnees.ressources.ferments_disponibles, "res_ferments")

        # --- PRODUITS ---
        ttk.Label(scrollable_frame, text="CARACTÉRISTIQUES DES PRODUITS", font=('Helvetica', 12, 'bold')).pack(pady=(20, 5), anchor='w')

        for i, prod in enumerate(self.donnees.produits):
            p_frame = ttk.LabelFrame(scrollable_frame, text=f"Produit {prod.code} - {prod.nom}")
            p_frame.pack(fill="x", padx=5, pady=5)

            self.add_entry(p_frame, "Lait (L/lot)", prod.lait_par_lot, f"p{i}_lait")
            self.add_entry(p_frame, "Sucre (kg/lot)", prod.sucre_par_lot, f"p{i}_sucre")
            self.add_entry(p_frame, "Ferments (kg/lot)", prod.ferments_par_lot, f"p{i}_ferments")
            self.add_entry(p_frame, "Profit (DH/lot)", prod.profit_par_lot, f"p{i}_profit")
            self.add_entry(p_frame, "Production minimale (lots)", prod.contrainte_min, f"p{i}_min")

        # Boutons
        btn_frame = ttk.Frame(scrollable_frame)
        btn_frame.pack(fill="x", pady=20)
        
        ttk.Button(btn_frame, text="Enregistrer", command=self.save_data).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Annuler", command=self.destroy).pack(side=tk.RIGHT, padx=5)

    def add_entry(self, parent, label, default_val, key):
        frame = ttk.Frame(parent)
        frame.pack(fill="x", padx=5, pady=2)
        ttk.Label(frame, text=label, width=25).pack(side=tk.LEFT)
        entry = ttk.Entry(frame)
        entry.insert(0, str(default_val))
        entry.pack(side=tk.RIGHT, fill="x", expand=True)
        self.entries[key] = entry

    def save_data(self):
        try:
            lait = float(self.entries["res_lait"].get())
            sucre = float(self.entries["res_sucre"].get())
            ferments = float(self.entries["res_ferments"].get())
            ressources = Ressources(lait, sucre, ferments)

            produits = []
            for i, prod in enumerate(self.donnees.produits):
                p_lait = float(self.entries[f"p{i}_lait"].get())
                p_sucre = float(self.entries[f"p{i}_sucre"].get())
                p_ferm = float(self.entries[f"p{i}_ferments"].get())
                p_prof = float(self.entries[f"p{i}_profit"].get())
                p_min = float(self.entries[f"p{i}_min"].get())
                
                produits.append(Produit(
                    prod.code, prod.nom, p_lait, p_sucre, p_ferm, p_prof, p_min
                ))

            nouvelles_donnees = DonneesProbleme(ressources, produits)
            set_donnees(nouvelles_donnees)
            messagebox.showinfo("Succès", "Les données ont été mises à jour avec succès !")
            self.destroy()

        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer uniquement des nombres valides.")


class LaitiereGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Optimisation Laitière - Interface Simple")
        self.geometry("1100x700")
        
        # Style
        self.style = ttk.Style(self)
        try:
            self.style.theme_use('clam')
        except:
            pass

        self.create_widgets()
        
        # Rediriger stdout vers la console texte
        self.redirector = RedirectText(self.console_text)
        sys.stdout = self.redirector

    def create_widgets(self):
        # Header
        header = ttk.Frame(self)
        header.pack(fill=tk.X, padx=10, pady=10)
        ttk.Label(header, text="Optimisation de la Production Laitière", font=('Helvetica', 18, 'bold')).pack()
        ttk.Label(header, text="Programmation Linéaire - EMSI").pack()

        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Menu Gauche
        left_frame = ttk.Frame(main_frame, width=250)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        btn_width = 30
        
        ttk.Label(left_frame, text="Exécution", font=('Helvetica', 12, 'bold')).pack(pady=(0, 10))
        ttk.Button(left_frame, text="1. Méthode Graphique (2 var)", width=btn_width, command=self.run_chap1).pack(pady=5)
        ttk.Button(left_frame, text="2. Méthode Simplexe (4 var)", width=btn_width, command=self.run_chap2).pack(pady=5)
        ttk.Button(left_frame, text="3. Exécuter les deux", width=btn_width, command=self.run_both).pack(pady=5)
        
        ttk.Separator(left_frame, orient='horizontal').pack(fill='x', pady=15)
        
        ttk.Label(left_frame, text="Données", font=('Helvetica', 12, 'bold')).pack(pady=(0, 10))
        ttk.Button(left_frame, text="Afficher les données", width=btn_width, command=self.show_data).pack(pady=5)
        ttk.Button(left_frame, text="Configurer les données", width=btn_width, command=self.configure_data).pack(pady=5)
        ttk.Button(left_frame, text="Réinitialiser", width=btn_width, command=self.reset_data).pack(pady=5)
        
        ttk.Separator(left_frame, orient='horizontal').pack(fill='x', pady=15)
        
        ttk.Button(left_frame, text="Effacer la console", width=btn_width, command=self.clear_console).pack(pady=5)
        ttk.Button(left_frame, text="Quitter", width=btn_width, command=self.quit_app).pack(pady=5)

        # Console Droite
        right_frame = ttk.LabelFrame(main_frame, text="Console de Sortie")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.console_text = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, font=('Consolas', 10), bg='#1e1e1e', fg='#00ff00')
        self.console_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.console_text.configure(state='disabled')

    def run_task(self, title, target):
        self.clear_console()
        print(f"Lancement de : {title}...\n")
        self.update_idletasks() # Force un rafraîchissement initial
        try:
            target()
        except Exception as e:
            print(f"\nErreur lors de l'exécution: {e}")

    def run_chap1(self):
        self.run_task("Chapitre 1 : Méthode Graphique", run_chapitre1)

    def run_chap2(self):
        self.run_task("Chapitre 2 : Méthode du Simplexe", run_chapitre2)

    def run_both(self):
        def task():
            print("=== CHAPITRE 1 ===")
            run_chapitre1()
            print("\n=== CHAPITRE 2 ===")
            run_chapitre2()
        self.run_task("Exécution complète", task)

    def show_data(self):
        self.clear_console()
        afficher_donnees_probleme()

    def configure_data(self):
        ConfigDialog(self)

    def reset_data(self):
        reinitialiser_donnees()
        messagebox.showinfo("Information", "Les données ont été réinitialisées avec succès.")
        self.clear_console()
        print("Données réinitialisées aux valeurs par défaut.")

    def clear_console(self):
        self.console_text.configure(state='normal')
        self.console_text.delete(1.0, tk.END)
        self.console_text.configure(state='disabled')

    def quit_app(self):
        # Rétablir stdout par sécurité avant de quitter
        sys.stdout = sys.__stdout__
        self.quit()
        self.destroy()

if __name__ == "__main__":
    app = LaitiereGUI()
    app.mainloop()
