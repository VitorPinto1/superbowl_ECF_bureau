import mysql.connector
from datetime import date, datetime

class BdLogique:
    # Methode pour initialiser la configuration de la base de données
    def __init__(self, config):
        self.config = config
    # Connexion base de donées
    def connect(self):
        return mysql.connector.connect(**self.config)

    def obtenir_tous_les_matchs(self):
        conn = self.connect()
        cursor = conn.cursor()
        query = "SELECT id, equipe1, equipe2, jour, debut, fin, cote1, cote2, commentaires, statut, score, but1, but2 FROM matchs"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

    def obtenir_donnees_du_jour(self):
        conn = self.connect()
        cursor = conn.cursor()
        date_actuelle = date.today()
        query = "SELECT id, equipe1, equipe2, jour, debut, fin, cote1, cote2, commentaires, statut, score, but1, but2  FROM matchs WHERE jour = %s"
        cursor.execute(query, (date_actuelle,))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

    def obtenir_mises(self, id_match):
        conn = self.connect()
        cursor = conn.cursor()
        query = "SELECT cote1, cote2, id_utilisateur FROM mises WHERE id_match = %s"
        cursor.execute(query, (id_match,))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

    def enregistrer_commentaires_et_score(self, id_match, commentaires, but1, but2):
        conn = self.connect()
        cursor = conn.cursor()
        query = "UPDATE matchs SET commentaires = %s, but1 = %s, but2 = %s WHERE id = %s"
        cursor.execute(query, (commentaires, but1, but2, id_match))
        conn.commit()
        cursor.close()
        conn.close()
      
    # Méthode pour clôturer un match en mettant à jour son statut et en déterminant le vainqueur
    def cloturer_partie(self, id_match):
        conn = self.connect()
        cursor = conn.cursor()
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
        conn.commit()
        cursor.close()
        conn.close()

    def mettre_a_jour_etat_matchs_en_cours(self):
        conn = self.connect()
        cursor = conn.cursor()
        date_heure_actuelles = datetime.now()
        requete = "UPDATE matchs SET statut = 'En cours' WHERE jour = %s AND debut <= %s AND fin >= %s"
        cursor.execute(requete, (date_heure_actuelles.date(), date_heure_actuelles.time(), date_heure_actuelles.time()))
        conn.commit()
        cursor.close()
        conn.close()
