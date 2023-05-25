# Développez une application Web en utilisant Django

## Scénario

Dans ce projet je travaille en tant que lead développeur Python pour la jeune startup LITReview.

Il m'est demandé de développer une application qui permet de demander ou publier des critiques de livres ou d’articles.

L’application présente deux cas d’utilisation principaux :

Les personnes qui demandent des critiques sur un livre ou sur un article particulier ;
Les personnes qui recherchent des articles et des livres intéressants à lire, en se basant sur les critiques des autres.
" Nous cherchons à mettre en place une application web pour notre MVP (minimum viable product, ou produit viable minimum). Je sais que tu as beaucoup d’expérience comme développeur Python, je pense que Django sera un framework idéal pour intégrer cette application. "

## Installation

1. Clonez le dépôt avec la commande `git clone https://github.com/SylvOne/projet9.git`.
2. Placez vous dans le dossier projet9 avec la commande `cd projet9`.
3. Créez un environnement virtuel avec la commande `python -m venv venv` sur Windows ou `python3 -m venv venv` sur Linux/Mac.
4. Activez l'environnement virtuel avec la commande `source venv/bin/activate` sur Linux/Mac ou `.\venv\scripts\activate` sur Windows.
5. Installez les dépendances avec `pip install -r requirements.txt`.

## Lancement du serveur

- Vous pouvez maintenant lancer le serveur localement avec la commande `python manage.py runserver`.
  ATTENTION : Il faudra garder le terminal qui a servi au lancement du serveur, ouvert.
  (Vous pourrez stopper le serveur en effectuant un Ctrl + C dans ce même terminal)

## Utilisation

- Pour accéder au site, ouvrez un navigateur et inscrivez cette URL dans la barre d'adresse : `http://127.0.0.1:8000`
  
Vous pouvez vous connecter directement avec les comptes suivants :

- Compte administrateur :
  - login : admin
  - mdp : litreview

- Comptes utilisateurs :
  - login : Tom
  - mdp : 1234

  - login : Sam
  - mdp : 1234
  
## Rapport Flake8-HTML

1. Générez un rapport Flake8-HTML avec la commande suivante :
`flake8 --exclude=.git,__pycache__,venv,migrations --max-line-length=119 --format=html --htmldir=flake8_rapport`.
2. Ouvrez le fichier `flake8_rapport/index.html` pour voir le rapport.
