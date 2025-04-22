# Superbowlapp Application Bureautique

Prérequis

- 	Visual Studio Code
-  	Extension Python pour VS Code
-  	Git
-  	Python 3.9
-  	MySQL: Le serveur de base de données MySQL doit être en cours d'exécution. AivenCloud
-  	Docker Desktop + XQuartz pour Mac

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


Information des archives 

- bd_logique.py : Gère les interactions avec la base de données.
- match_logique.py : Contient la logique de l'application pour la gestion des matchs.
- main.py : Fichier principal pour démarrer l'application et gérer l'interface utilisateur.
- Dockerfile : Fichier pour construire l'image Docker.
- docker-compose.yml : Lancement rapide de l'application avec Docker Compose.
- requirements.txt : Liste des dépendances Python.


Déploiement avec Docker

Prérequis :

- Docker Desktop installé

- (Sur Mac) Installer XQuartz et lancer xhost + pour activer l'affichage X11.

Sur Mac, avant de lancer l'application :

	« xhost + »

(Si besoin, récupérer votre IP locale avec ipconfig getifaddr en0.)

Lancer l'application avec Docker Compose

	« docker-compose up »

Construction manuelle 
Construire et lancer sans docker-compose :

	«	docker build -t superbowlapp-bureau .
		docker run -it --rm \
			-e DISPLAY=host.docker.internal:0 \
			-v /tmp/.X11-unix:/tmp/.X11-unix \
			superbowlapp-bureau »

(Sur Mac M1/M2 ➔ remplacer host.docker.internal par votre IP locale.)

CI/CD à chaque git push sur main :

- L'image Docker est automatiquement construite avec GitHub Actions

- L'image est poussée sur DockerHub sous : vitorpinto500/superbowlapp-bureau:latest

Auteur

Projet réalisé par Vitor Pinto Passionné par le développement et l'IA.