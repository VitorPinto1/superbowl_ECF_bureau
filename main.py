import mysql.connector
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from datetime import date
from ttkthemes import ThemedTk
from dotenv import load_dotenv
from tkinter import PhotoImage
from tkinter import Canvas
from PIL import Image, ImageTk


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



# Variable pour stocker l'ID du match sélectionné
id_match_selection = None
entry_commentaires = None
lbl_erreur = None

def obtenir_tous_les_matchs():
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    query = "SELECT id, equipe1, equipe2, jour, debut, fin, cote1, cote2, commentaires, statut, score, but1, but2 FROM matchs"
    cursor.execute(query)

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results

def charger_donnes(tipo):
    if tipo == "du_jour":
        datos = obtenir_donnees_du_jour()
    else:
        datos = obtenir_tous_les_matchs()

    # Efface les données de la table avant de charger les nouvelles
    for i in table_matchs.get_children():
        table_matchs.delete(i)

    # Insérer les données dans la table
    for row in datos:
        table_matchs.insert("", tk.END, text=row[0], values=row[1:])


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

def afficher_message(message):
    global lbl_erreur
    
    if lbl_erreur is not None:
        lbl_erreur.destroy()  # Détruire le widget existant s'il y en a un
    
    lbl_erreur = tk.Label(frame_inputs, fg="red", text=message)
    lbl_erreur.pack()

# Fonction pour enregistrer les commentaires et le score d'un match
def enregistrer_commentaires_et_score(id_match, commentaires, but1, but2):
    global lbl_erreur
    
    if not commentaires or not but1 and but2:
        # Afficher un message d'erreur si l'un des champs est vide
        afficher_message("Veuillez remplir tous les champs avant d'enregistrer.")
        return
    try:
            but1_num = int(but1)
            but2_num = int(but2)
            if not (0 <= but1_num <= 20 and 0 <= but2_num <= 20):
                afficher_message("Les scores doivent être des nombres entre 0 et 20.")
                return
    except ValueError:
            afficher_message("Les scores doivent être des nombres entre 0 et 20.")
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

    afficher_message("Commentaires et score enregistrés avec succès.")

    fenetre.after(2000, lambda: afficher_message(""))


# Fonction pour nettoyer la fenêtre des données du match
def nettoyer_fenetre_donnees_match():
    global id_match_selection, entry_commentaires, frame_inputs

    id_match_selection = None

   
    for widget in frame_inputs.winfo_children():
        widget.destroy()

# Fonction pour gérer la sélection d'un match
def selectionner_match(event):
    global id_match_selection, entry_commentaires, frame_inputs

    if frame_inputs is not None:
        frame_inputs.pack(pady=10)

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
        lbl_cote1 = ttk.Label(frame_inputs, text="Cote " + equipe1 + " = " + str(cote1))
        lbl_cote1.pack()

        lbl_cote2 = ttk.Label(frame_inputs, text="Cote " + equipe2 + " = " + str(cote2))
        lbl_cote2.pack()

        for equipe, compte in equipes_mises.items():
            text_label_selection = "Nombre de mises pour " + equipe + ": " + str(compte)
            lbl_equipe = ttk.Label(frame_inputs, text=text_label_selection)
            lbl_equipe.pack()

        # Étiquette et champ de saisie pour les commentaires
        lbl_commentaires = ttk.Label(frame_inputs, text="Commentaires:")
        lbl_commentaires.pack()
        entry_commentaires = ttk.Entry(frame_inputs)
        entry_commentaires.pack()

        
        # Étiquette et champ de saisie pour le score
        lbl_but1 = ttk.Label(frame_inputs, text="Score : " + equipe1)
        lbl_but1.pack()
        entry_but1 = ttk.Entry(frame_inputs)
        entry_but1.pack()

        # Étiquette et champ de saisie pour le score
        lbl_but2 = ttk.Label(frame_inputs, text="Score : " + equipe2)
        lbl_but2.pack()
        entry_but2 = ttk.Entry(frame_inputs)
        entry_but2.pack()

        # Bouton pour enregistrer les commentaires et le score
        btn_enregistrer = ttk.Button(frame_inputs, text="Enregistrer", command=lambda: enregistrer_commentaires_et_score(id_match, entry_commentaires.get(), entry_but1.get(), entry_but2.get()))
        btn_enregistrer.pack()

        # Bouton cloturer match
        btn_cloturer = ttk.Button(frame_inputs, text="Cloturer", command=lambda: cloturer_partie(id_match))
        btn_cloturer.pack()

        # Bouton sortir match
        btn_sortir = ttk.Button(frame_inputs, text="Sortir", command=sortir)
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

        # Mettre à jour la fenêtre avec les modifications
        nettoyer_fenetre_donnees_match()
        

        # Message de succès
        afficher_message("Match cloturé")

        fenetre.after(2000, lambda: afficher_message(""))

       
    else:
        # Message d'erreur si aucun match n'a été sélectionné
        afficher_message("Veuillez sélectionner un match avant de clore.")



def sortir():
    global id_match_selection, frame_inputs
    nettoyer_fenetre_donnees_match()
    frame_inputs.pack_forget()
    id_match_selection = None
   




# Créer la fenêtre de l'application

fenetre = ThemedTk(theme="adapta") 
fenetre.title("Matchs")
fenetre.geometry("1200x900")
fenetre.minsize(1000,800)


# Charger l'image de fond
background_image = Image.open("Ressources/background3.jpg")
background_image = background_image.resize((fenetre.winfo_screenwidth(), fenetre.winfo_screenheight()), Image.LANCZOS)

background_image = ImageTk.PhotoImage(background_image)

# Créer un widget Label pour afficher l'image
label_fondo = tk.Label(fenetre, image=background_image)
label_fondo.place(relwidth=1, relheight=1)

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


frame_boutons = tk.Frame(fenetre, background= "black")
frame_boutons.pack(pady=10)

# Créer les boutons et les ajouter au cadre
btn_du_jour = ttk.Button(frame_boutons, text="Matchs du Jour", command=lambda: charger_donnes("du_jour"))
btn_du_jour.pack(side=tk.LEFT, padx=10, pady=50)  # Utiliser side=tk.LEFT pour aligner horizontalement

btn_tous_les_matchs = ttk.Button(frame_boutons, text="Tous les matchs", command=lambda: charger_donnes("tous"))
btn_tous_les_matchs.pack(side=tk.LEFT, padx=10, pady=50)





# Configurer les colonnes pour qu'elles soient fixes et non modifiables
largeurs_colonnes = {"equipe1": 200, "equipe2": 200, "jour": 100, "debut": 100, "fin": 100}
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