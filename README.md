# Superbowlapp Application Bureautique

Prérequis

- 	Visual Studio Code
-  	Extension Python pour VS Code
-  	Git
-  	Python 3.9
-  	MySQL: Le serveur de base de données MySQL doit être en cours d'exécution. AivenCloud

1. Installation et déploiement

Lancez VSCode et installez l’extension « Python » publiée par Microsoft. Après avoir créé le dossier 'superbowl_bureau'. Ouvrez un terminal intégré dans VS Code pour faire le clonage du dépôt et exécuter les commandes suivantes :

  	« git clone https://github.com/VitorPinto1/superbowl_ECF_bureau.git »
  	« cd superbowl_bureau »
   
2. Configuration de l'environnement

Activez l'environnement virtuel Python dans le terminal :

  	« source env/bin/activate »  # Sur Unix ou MacOS
  	« env\Scripts\activate »    # Sur Windows

Si l'environnement virtuel n'existe pas encore, vous pouvez le créer avec :

  	« python -m venv env » 

3. Installer les dépendances

Installez les paquets nécessaires à partir du fichier requirements.txt si disponible.

  	« pip install -r requirements.txt »

4. Lancement de l’application

Exécutez l’application  dans le teminal :

  	« python main.py »

5. Accéder à l’application

En suivant ces étapes, vous devriez être en mesure de déployer l'application bureautique localement et tester ses fonctionnalités.


# Information des archives 

- bd_logique.py : Gère les interactions avec la base de données.
- match_logique.py : Contient la logique de l'application pour la gestion des matchs.
- main.py : Fichier principal pour démarrer l'application et gérer l'interface utilisateur.



