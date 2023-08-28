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
entry_commentaires = None
lbl_erreur = None
# Fonction pour obtenir les données de la table "matchs"
def obtenir_donnees_du_jour():
    # Connexion à la base de données
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # Obtenir la date actuelle
    date_actuelle = date.today()

    # Exécution de la requête
    query = "SELECT id, equipe1, equipe2, jour, debut, fin, cote1, cote2, commentaires, statut, score  FROM matchs WHERE jour = %s"
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

def afficher_message_erreur(message):
    global lbl_erreur
    
    if lbl_erreur is not None:
        lbl_erreur.destroy()  # Destruir el widget existente si hay uno
    
    lbl_erreur = tk.Label(frame_inputs, fg="red", text=message)
    lbl_erreur.pack()
# Fonction pour enregistrer les commentaires et le score d'un match
def enregistrer_commentaires_et_score(id_match, commentaires, score):
    global lbl_erreur
    
    if not commentaires or not score:
        # Afficher un message d'erreur si l'un des champs est vide
        afficher_message_erreur("Veuillez remplir tous les champs avant d'enregistrer.")
        return

    
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

    nettoyer_fenetre_donnees_match()

# Fonction pour nettoyer la fenêtre des données du match
def nettoyer_fenetre_donnees_match():
    global id_match_selection, entry_commentaires, frame_inputs

    id_match_selection = None

    # Nettoyer la fenêtre des données du match
    for widget in frame_inputs.winfo_children():
        widget.destroy()

# Fonction pour gérer la sélection d'un match
def selectionner_match(event):
    global id_match_selection, entry_commentaires, frame_inputs

    selected_items = table_matchs.selection()
    if selected_items:
        item = selected_items[0]

        if id_match_selection is None:
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

            # Enregistrer l'ID du match sélectionné
            id_match_selection = id_match

            # Obtener les résultats
            obtenir_donnes = obtenir_donnees_du_jour()

            for result in obtenir_donnes:
                equipe1, equipe2, cote1, cote2, commentaires, score = result[1], result[2], result[6], result[7], result[8], result[10]


            # Créer des étiquettes pour afficher les cotisations
            lbl_cote1 = tk.Label(frame_inputs, text="Cote " + equipe1 + " = " + str(cote1))
            lbl_cote1.pack()

            lbl_cote2 = tk.Label(frame_inputs, text="Cote " + equipe2 + " = " + str(cote2))
            lbl_cote2.pack()

        

           

            for equipe, compte in equipes_mises.items():
                text_label_selection = "Nombre de mises pour " + equipe + ": " + str(compte)
                lbl_equipe = tk.Label(frame_inputs, text=text_label_selection)
                lbl_equipe.pack()

            # Étiquette et champ de saisie pour les commentaires
            lbl_commentaires = tk.Label(frame_inputs, text="Commentaires:")
            lbl_commentaires.pack()
            entry_commentaires = tk.Entry(frame_inputs)
            entry_commentaires.pack()

            # Étiquette et champ de saisie pour le score
            lbl_score = tk.Label(frame_inputs, text="Score:")
            lbl_score.pack()
            entry_score = tk.Entry(frame_inputs)
            entry_score.pack()

            # Bouton pour enregistrer les commentaires et le score
            btn_enregistrer = tk.Button(frame_inputs, text="Enregistrer", command=lambda: enregistrer_commentaires_et_score(id_match, entry_commentaires.get(), entry_score.get()))
            btn_enregistrer.pack()

            # Bouton cloturer match
            btn_cloturer = tk.Button(frame_inputs, text="Cloturer", command=lambda: cloturer_partie(id_match))
            btn_cloturer.pack()

          

    else:
        nettoyer_fenetre_donnees_match()


def cloturer_partie(id_match):
    global id_match_selection

    if id_match_selection is not None:
        # Connexion a la base de datos
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Mise à jour de l'état "fin" du match à "Terminé"
        query = "UPDATE matchs SET statut = %s WHERE id = %s"
        cursor.execute(query, ("Terminé", id_match_selection))

        # Enregistrer les modifications dans la base de données
        conn.commit()

        # Fermeture du curseur et de la connexion
        cursor.close()
        conn.close()

        # Actualizar la ventana con los cambios
        nettoyer_fenetre_donnees_match()
        

        # Mensaje de éxito
        afficher_message_erreur("Match cloturé")

        fenetre.after(2000, lambda: afficher_message_erreur(""))
    else:
        # Mensaje de error si no se ha seleccionado ningún partido
        afficher_message_erreur("Veuillez sélectionner un match avant de clore.")





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

# selection de match
table_matchs.bind("<Button-1>", selectionner_match)

# Obtenir les données de la table "matchs"
donnees_matchs_actuels = obtenir_donnees_du_jour()

# Insérer les données dans l'arbre de données
for row in donnees_matchs_actuels:
    table_matchs.insert("", tk.END, text=row[0], values=row[1:])

# Pack the treeview
table_matchs.pack()

# Frame pour afficher les informations du match sélectionné
frame_inputs = ttk.Frame(fenetre)
frame_inputs.pack(pady=10)

# Démarrer la boucle d'événements de l'application
fenetre.mainloop()
