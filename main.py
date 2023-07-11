import mysql.connector
import tkinter as tk
from tkinter import ttk
from datetime import date
from ttkthemes import ThemedTk

# Configuration de la base de données
config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'PEPE',
    'password': 'PEPE',
    'database': 'bdsuperbowl'
}

# Variable para almacenar el ID del partido seleccionado
id_match_selection = None

# Fonction pour obtenir les données de la table "matchs"
def obtenir_donnees_du_jour():
    # Connexion à la base de données
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # Obtenir la date actuelle
    date_actuelle = date.today()

    # Exécution de la requête
    query = "SELECT id, equipe1, equipe2, jour, debut, fin FROM matchs WHERE jour = %s"
    cursor.execute(query, (date_actuelle,))

    # Obtenir les résultats
    results = cursor.fetchall()

    # Fermeture du curseur et de la connexion
    cursor.close()
    conn.close()

    return results

# Fonction pour obtenir les données de mise pour un match spécifique
def obtenir_mises(id_match):
    # Connexion à la base de données
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # Exécution de la requête
    query = "SELECT cote1, cote2, id_utilisateur FROM mises WHERE id_match = %s"
    cursor.execute(query, (id_match,))

    # Obtenir les résultats
    results = cursor.fetchall()

    # Fermeture du curseur et de la connexion
    cursor.close()
    conn.close()

    return results

# Fonction pour enregistrer les commentaires et le score d'un match
def commentaires_et_score(id_match, commentaires, score):
    # Connexion à la base de données
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # Mise à jour du match avec les commentaires et le score
    query = "UPDATE matchs SET commentaires = %s, score = %s WHERE id = %s"
    cursor.execute(query, (commentaires, score, id_match))

    # Enregistrer les modifications dans la base de données
    conn.commit()

    # Fermeture du curseur et de la connexion
    cursor.close()
    conn.close()

# Fonction pour gérer la sélection d'un match
def selectionner_match(event):
    global id_match_selection
    if id_match_selection is None:
        item = table_matchs.selection()[0]
        id_match = table_matchs.item(item, 'text')
        values = table_matchs.item(item, 'values')

        # Obtenir les données de mise pour le match sélectionné
        donnees_mises = obtenir_mises(id_match)

        # Créer un dictionnaire pour stocker les équipes et leurs comptes de mises
        equipes_mises = {values[0]: 0, values[1]: 0}

        # Compter les mises par équipe
        for cote1, cote2, id_utilisateur in donnees_mises:
            if cote1:
                equipes_mises[values[0]] += 1  # Équipe 1
            if cote2:
                equipes_mises[values[1]] += 1  # Équipe 2

        # Afficher les données de mise
        print("Match sélectionné:", values)
        for equipe, compte in equipes_mises.items():
            print("Équipe:", equipe)
            print("Nombre de mises:", compte)

        # Enregistrer l'ID du match sélectionné
        id_match_selection = id_match

        # Créer des étiquettes pour afficher les cotisations
        lbl_cote1 = tk.Label(fenetre, text="Cote 1: " + str(cote1))
        lbl_cote1.pack()

        lbl_cote2 = tk.Label(fenetre, text="Cote 2: " + str(cote2))
        lbl_cote2.pack()

        lbl_equipe = tk.Label(fenetre, text= equipe)
        lbl_equipe.pack()

        lbl_compte = tk.Label(fenetre, text= compte)
        lbl_compte.pack()


        


        # Créer une nouvelle fenêtre pour saisir les commentaires et le score
        frame_inputs = ttk.Frame(fenetre)
        frame_inputs.pack(pady=10)

        # Étiquette et champ de saisie pour les commentaires
        lbl_commentaires = tk.Label(frame_inputs, text="Commentaires:")
        lbl_commentaires.grid(row=0, column=0, sticky=tk.E)
        entry_commentaires = tk.Entry(frame_inputs)
        entry_commentaires.grid(row=0, column=1)

        # Étiquette et champ de saisie pour le score
        lbl_score = tk.Label(frame_inputs, text="Score:")
        lbl_score.grid(row=1, column=0, sticky=tk.E)
        entry_score = tk.Entry(frame_inputs)
        entry_score.grid(row=1, column=1)

        # Fonction pour enregistrer les commentaires et le score en appuyant sur un bouton
        def enregistrer_commentaires_et_score():
            commentaires = entry_commentaires.get()
            score = entry_score.get()

            # Enregistrer les commentaires et le score dans la base de données
            commentaires_et_score(id_match, commentaires, score)

            # Réinitialiser l'ID du match sélectionné
            id_match_selection = None

            # Détruire le frame_inputs
            frame_inputs.destroy()

            
        # Bouton pour enregistrer les commentaires et le score
        btn_enregistrer = tk.Button(fenetre, text="Enregistrer", command=enregistrer_commentaires_et_score)
        btn_enregistrer.pack()

# Créer la fenêtre de l'application
fenetre = ThemedTk(theme="default")
fenetre.title("Matchs")

# Créer un arbre de données avec un style amélioré
style = ttk.Style(fenetre)
style.configure("Custom.Treeview", highlightthickness=0, bd=0)
style.configure("Custom.Treeview.Heading", font=('Helvetica', 10, 'bold'))
table_matchs = ttk.Treeview(fenetre, columns=("equipe1", "equipe2", "jour", "debut", "fin"), style="Custom.Treeview")
table_matchs["columns"] = ("equipe1", "equipe2", "jour", "debut", "fin")

table_matchs["show"] = "headings"

# Désactiver le redimensionnement des colonnes
table_matchs.bind("<Button-1>", selectionner_match)

# Définir les en-têtes des colonnes
table_matchs.heading("equipe1", text="Équipe 1")
table_matchs.heading("equipe2", text="Équipe 2")
table_matchs.heading("jour", text="Jour")
table_matchs.heading("debut", text="Début")
table_matchs.heading("fin", text="Fin")

# Configurer les colonnes pour qu'elles soient fixes et non modifiables
largeurs_colonnes = {"equipe1": 100, "equipe2": 100, "jour": 100, "debut": 100, "fin": 100}
for colonne, largeur in largeurs_colonnes.items():
    table_matchs.column(colonne, width=largeur, anchor=tk.CENTER)

# Obtenir les données de la table "matchs"
donnees_matchs_actuels = obtenir_donnees_du_jour()

# Insérer les données dans l'arbre de données
for row in donnees_matchs_actuels:
    id_match, *values = row
    table_matchs.insert("", tk.END, text=id_match, values=values[:5])  # 5 valeurs

# Pack the treeview
table_matchs.pack()

# Démarrer la boucle d'événements de l'application
fenetre.mainloop()
