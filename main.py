import mysql.connector
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from datetime import date
from ttkthemes import ThemedTk
from dotenv import load_dotenv

import os
load_dotenv ()
# Configuration de la base de données
config = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT')),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_DATABASE')
}



# Variable para almacenar el ID del partido seleccionado
id_match_selection = None
entry_commentaires = None
lbl_erreur = None

def mettre_a_jour_etat_matchs_en_cours():
    # Connexion à la base de données
    conn = mysql.connector.connect(**config)
    curseur = conn.cursor()

    # Obtenir la date et l'heure actuelles
    date_heure_actuelles = datetime.now()

    # Mettre à jour l'état des matchs en cours
    requete = "UPDATE matchs SET statut = 'En cours' WHERE jour = %s AND debut <= %s AND fin >= %s"
    curseur.execute(requete, (date_heure_actuelles.date(), date_heure_actuelles.time(), date_heure_actuelles.time()))

    # Enregistrer les modifications dans la base de données
    conn.commit()

    # Fermer le curseur et la connexion
    curseur.close()
    conn.close()

# Appeler la fonction pour mettre à jour l'état des matchs en cours au début
mettre_a_jour_etat_matchs_en_cours()

# Fonction pour obtenir les données de la table "matchs"
def obtenir_donnees_du_jour():
    # Connexion à la base de données
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # Obtenir la date actuelle
    date_actuelle = date.today()

    # Exécution de la requête
    query = "SELECT id, equipe1, equipe2, jour, debut, fin, cote1, cote2, commentaires, statut, score, but1, but2  FROM matchs WHERE jour = %s"
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
def enregistrer_commentaires_et_score(id_match, commentaires, but1, but2):
    global lbl_erreur
    
    if not commentaires or not but1 and but2:
        # Afficher un message d'erreur si l'un des champs est vide
        afficher_message_erreur("Veuillez remplir tous les champs avant d'enregistrer.")
        return

    
    # Connexion à la base de données
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # Mise à jour du match avec les commentaires et le score
    query = "UPDATE matchs SET commentaires = %s, but1 = %s, but2 = %s WHERE id = %s"
    cursor.execute(query, (commentaires, but1, but2, id_match))

    # Enregistrer les modifications dans la base de données
    conn.commit()

    # Fermeture du curseur et de la connexion
    cursor.close()
    conn.close()

    nettoyer_fenetre_donnees_match()

    afficher_message_erreur("Commentaires et score enregistrés avec succès.")

    fenetre.after(2000, lambda: afficher_message_erreur(""))


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

        # Nettoyer la fenêtre des données du match
        nettoyer_fenetre_donnees_match()

        # Obtener les résultats
        equipe1, equipe2, cote1, cote2 = values[0], values[1], values[5], values[6] 


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
        lbl_but1 = tk.Label(frame_inputs, text="Score : " + equipe1)
        lbl_but1.pack()
        entry_but1 = tk.Entry(frame_inputs)
        entry_but1.pack()

        # Étiquette et champ de saisie pour le score
        lbl_but2 = tk.Label(frame_inputs, text="Score : " + equipe2)
        lbl_but2.pack()
        entry_but2 = tk.Entry(frame_inputs)
        entry_but2.pack()

        # Bouton pour enregistrer les commentaires et le score
        btn_enregistrer = tk.Button(frame_inputs, text="Enregistrer", command=lambda: enregistrer_commentaires_et_score(id_match, entry_commentaires.get(), entry_but1.get(), entry_but2.get()))
        btn_enregistrer.pack()

        # Bouton cloturer match
        btn_cloturer = tk.Button(frame_inputs, text="Cloturer", command=lambda: cloturer_partie(id_match))
        btn_cloturer.pack()

        # Bouton sortir match
        btn_sortir = tk.Button(frame_inputs, text="Sortir", command=sortir)
        btn_sortir.pack()

    else:
        nettoyer_fenetre_donnees_match()
        



def cloturer_partie(id_match):
    if id_match is not None:
        # Connexion a la base de données
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Mise à jour de l'état "fin" du match à "Terminé"
        query = "UPDATE matchs SET statut = %s WHERE id = %s"
        cursor.execute(query, ("Terminé", id_match))

        query_vainqueur = """
            UPDATE matchs
            SET vainqueur = CASE
                WHEN but1 > but2 THEN equipe1
                WHEN but1 < but2 THEN equipe2
                ELSE '-'
            END
            WHERE id = %s;
        """
        cursor.execute(query_vainqueur, (id_match,))

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



def sortir():
    global id_match_selection
    nettoyer_fenetre_donnees_match()
    id_match_selection = None



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


