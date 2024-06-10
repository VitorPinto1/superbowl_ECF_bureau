import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from dotenv import load_dotenv
from PIL import Image, ImageTk
from bd_logique import BdLogique  
from match_logique import MatchLogique 
import os

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()
config = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT')),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_DATABASE')
}


class BureauApp:
    # Méthode pour initialiser la logique des matchs
    def __init__(self, match_logique):
        self.match_logique = match_logique
        self.id_match_selection = None
        self.entry_commentaires = None
        self.lbl_erreur = None
        self.setup_gui()

    def setup_gui(self):
        self.fenetre = ThemedTk(theme="adapta")
        self.fenetre.title("Matchs")
        self.fenetre.geometry("1200x900")
        self.fenetre.minsize(1000, 800)

        background_image = Image.open("Ressources/background3.jpg")
        background_image = background_image.resize((self.fenetre.winfo_screenwidth(), self.fenetre.winfo_screenheight()), Image.LANCZOS)
        self.background_image = ImageTk.PhotoImage(background_image)
        self.label_background = tk.Label(self.fenetre, image=self.background_image)
        self.label_background.place(relwidth=1, relheight=1)

        self.setup_buttons()

        self.table_matchs = ttk.Treeview(self.fenetre, columns=("equipe1", "equipe2", "jour", "debut", "fin"), style="Custom.Treeview")
        self.setup_table()  

        self.frame_inputs = ttk.Frame(self.fenetre)
        self.frame_inputs.pack(pady=10)

        self.match_logique.mettre_a_jour_etat_matchs_en_cours()
        self.data_charge("du_jour")

        self.fenetre.mainloop()
    
    def setup_table(self):
        style = ttk.Style(self.fenetre)
        style.configure("Custom.Treeview", highlightthickness=0, bd=0)
        style.configure("Custom.Treeview.Heading", font=('Helvetica', 10, 'bold'))
        self.table_matchs["show"] = "headings"
        self.table_matchs.heading("equipe1", text="Équipe 1")
        self.table_matchs.heading("equipe2", text="Équipe 2")
        self.table_matchs.heading("jour", text="Jour")
        self.table_matchs.heading("debut", text="Début")
        self.table_matchs.heading("fin", text="Fin")

        self.column_widths = {"equipe1": 200, "equipe2": 200, "jour": 200, "debut": 200, "fin": 200}
        for column, width in self.column_widths.items():
            self.table_matchs.column(column, width=width, anchor=tk.CENTER, stretch=False)

        self.table_matchs.bind("<Configure>", self.prevent_resize)
        self.table_matchs.bind("<ButtonRelease-1>", self.prevent_resize_click)
        self.table_matchs.bind("<Motion>", self.prevent_resize)

        self.table_matchs.pack()
        self.table_matchs.bind("<Button-1>", self.selectionner_match)
      
   
    # Méthode pour empêcher les colonnes de la table de changer de taille
    def prevent_resize(self, event):
        for col in self.table_matchs["columns"]:
            self.table_matchs.column(col, width=self.column_widths[col], stretch=False)

    def prevent_resize_click(self, event):
        if self.table_matchs.identify_region(event.x, event.y) == "separator":
            return "break"
        self.prevent_resize(event)
        
    def setup_buttons(self):
        button_frame = tk.Frame(self.fenetre, background="black")
        button_frame.pack(pady=10)
        btn_du_jour = ttk.Button(button_frame, text="Matchs du Jour", command=lambda: self.data_charge("du_jour"))
        btn_du_jour.pack(side=tk.LEFT, padx=10, pady=50)
        btn_tous_les_matchs = ttk.Button(button_frame, text="Tous les matchs", command=lambda: self.data_charge("tous"))
        btn_tous_les_matchs.pack(side=tk.LEFT, padx=10, pady=50)

    def afficher_message(self, message):
        if self.lbl_erreur is not None:
            self.lbl_erreur.destroy()
        self.lbl_erreur = tk.Label(self.frame_inputs, fg="red", text=message)
        self.lbl_erreur.pack()
        self.fenetre.after(2000, lambda: self.lbl_erreur.destroy())

    # Méthode pour charger les données des matchs en fonction du type spécifié
    def data_charge(self, tipe):
        data = self.match_logique.charger_donnes(tipe)
        for i in self.table_matchs.get_children():
            self.table_matchs.delete(i)
        for row in data:
            self.table_matchs.insert("", tk.END, text=row[0], values=row[1:])

    # Méthode pour gérer la sélection d'un match dans la table
    def selectionner_match(self, event):
        selected_items = self.table_matchs.selection()
        if selected_items:
            item = selected_items[0]
            id_match = self.table_matchs.item(item, 'text')
            values = self.table_matchs.item(item, 'values')

            self.id_match_selection = id_match
            self.nettoyer_fenetre_donnees_match()

            equipe1, equipe2, cote1, cote2 = values[0], values[1], values[5], values[6]
            lbl_cote1 = ttk.Label(self.frame_inputs, text="Cote " + equipe1 + " = " + str(cote1))
            lbl_cote1.pack()
            lbl_cote2 = ttk.Label(self.frame_inputs, text="Cote " + equipe2 + " = " + str(cote2))
            lbl_cote2.pack()

            bets_data = self.match_logique.obtenir_mises(id_match)
            teams_bets = {values[0]: 0, values[1]: 0}

            for cote1, cote2, id_utilisateur in bets_data:
                if cote1:
                    teams_bets[values[0]] += 1
                if cote2:
                    teams_bets[values[1]] += 1

            for team, count in teams_bets.items():
                lbl_team = ttk.Label(self.frame_inputs, text="Nombre de mises pour " + team + ": " + str(count))
                lbl_team.pack()

            # Champs de saisie pour les commentaires et les scores
            lbl_commentaires = ttk.Label(self.frame_inputs, text="Commentaires:")
            lbl_commentaires.pack()
            self.entry_commentaires = ttk.Entry(self.frame_inputs)
            self.entry_commentaires.pack()

            lbl_but1 = ttk.Label(self.frame_inputs, text="Score : " + equipe1)
            lbl_but1.pack()
            champ_but1 = ttk.Entry(self.frame_inputs)
            champ_but1.pack()

            lbl_but2 = ttk.Label(self.frame_inputs, text="Score : " + equipe2)
            lbl_but2.pack()
            champ_but2 = ttk.Entry(self.frame_inputs)
            champ_but2.pack()

            btn_save = ttk.Button(self.frame_inputs, text="Enregistrer", command=lambda: self.sauvegarder_details_match(id_match, self.entry_commentaires.get(), champ_but1.get(), champ_but2.get()))
            btn_save.pack()

            btn_fermer = ttk.Button(self.frame_inputs, text="Cloturer", command=lambda: self.fermer_match(id_match))
            btn_fermer.pack()

            btn_sortir = ttk.Button(self.frame_inputs, text="Sortir", command=self.exit)
            btn_sortir.pack()
        else:
            self.nettoyer_fenetre_donnees_match()

    # Méthode pour nettoyer les données affichées dans la fenêtre de détails du match
    def nettoyer_fenetre_donnees_match(self):
        self.id_match_selection = None
        for widget in self.frame_inputs.winfo_children():
            widget.destroy()

    # Méthode pour enregistrer les commentaires et les scores pour un match donné
    def sauvegarder_details_match(self, id_match, comments, goals_team1, goals_team2):
        if not comments or not goals_team1 or not goals_team2:
            self.afficher_message("Veuillez remplir tous les champs avant d'enregistrer.")
            return
        try:
            goals_team1 = int(goals_team1)
            goals_team2 = int(goals_team2)
            if not (0 <= goals_team1 <= 20 and 0 <= goals_team2 <= 20):
                self.afficher_message("Les scores doivent être des nombres entre 0 et 20.")
                return
        except ValueError:
            self.afficher_message("Les scores doivent être des nombres entre 0 et 20.")
            return

        self.match_logique.enregistrer_commentaires_et_score(id_match, comments, goals_team1, goals_team2)
        self.nettoyer_fenetre_donnees_match()
        self.afficher_message("Commentaires et score enregistrés avec succès.")

    # Méthode pour clôturer un match en mettant à jour son statut
    def fermer_match(self, id_match):
        if id_match is not None:
            self.match_logique.cloturer_partie(id_match)
            self.nettoyer_fenetre_donnees_match()
            self.afficher_message("Match cloturé")
        else:
            self.afficher_message("Veuillez sélectionner un match avant de clore.")
            
    # Méthode pour sortir de la fenêtre des détails du match
    def exit(self):
        self.nettoyer_fenetre_donnees_match()
        self.frame_inputs.pack_forget()
        self.id_match_selection = None

  

if __name__ == "__main__":
    bd_logique = BdLogique(config)
    match_logique = MatchLogique(bd_logique)
    app = BureauApp(match_logique)

