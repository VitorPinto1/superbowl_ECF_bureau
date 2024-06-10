class MatchLogique:
    # Méthode pour initialiser la logique de match avec l'accès à la base de données (bd_logique)
    def __init__(self, bd_logique):
        self.bd_logique = bd_logique

    # Méthode pour charger les données des matchs en fonction du type spécifié; du jour, tous
    def charger_donnes(self, tipe):
        if tipe == "du_jour":
            return self.bd_logique.obtenir_donnees_du_jour()
        else:
            return self.bd_logique.obtenir_tous_les_matchs()

    def obtenir_mises(self, id_match):
        return self.bd_logique.obtenir_mises(id_match)

    def enregistrer_commentaires_et_score(self, id_match, commentaires, but1, but2):
        self.bd_logique.enregistrer_commentaires_et_score(id_match, commentaires, but1, but2)

    def cloturer_partie(self, id_match):
        self.bd_logique.cloturer_partie(id_match)

    def mettre_a_jour_etat_matchs_en_cours(self):
        self.bd_logique.mettre_a_jour_etat_matchs_en_cours()
