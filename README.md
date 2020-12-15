# Plateforme prêt matériels électronique / équipements

## Installation

git
python 3 (with pip)
yarn

### Django
ouvrir un terminal,
se positionner à la racine. 

Installer les librairies python3 > pip et virtualenv

> sudo apt-get update
> sudo apt-get -y upgrade

> python3 -v
> sudo apt-get install -y 
> python3-pip
> sudo apt-get install 
> build-essential libssl-dev 
> libffi-dev python-dev

> sudo apt-get install -y python3-venv

Cloner le dépôt
> git clone https://gricad-gitlab.univ-grenoble-alpes.fr/fabmstic/platepret.git

se positionner dans la branche dev :

> git checkout dev

activer l’environnement virtuel

> python3 -m virtualenv venv

source venv/bin/activate

installer les dépendances :

> sudo pip3 install -r requirements.txt

### settings

Adapter les variables d'environnement situées dans Djangovue > settings.py

> CAS_SERVER_URL (url du service CAS)
> ALLOWED_HOSTS (domaines autorisés en développement)
-
> CORS_ORIGIN_WHITELIST (domaines autorisés pour les accès CORS)

lancer les migrations

> sudo python3 manage.py makemigrations
…

> sudo python3 manage.py migrate

démarrer le serveur

> sudo python3 manage.py runserver

### authentification

### création d’un superutilisateur
> une fois l’installation de Django effectuée, la création d’un utilisateur se fait avec le shell :
ouvrir un terminal et se placer à la racine du projet

- sudo python3 manage.py createsuperuser --username=joe --email=joe@example.com
 
### création d’un administrateur
> depuis l’interface d’administration, http://localhost:8000/admin
se loguer avec l’identifiant superutilisateur, puis ajouter des utilisateur depuis  « Users » 
Ajouter les permissions __Staff status__.


### login

> login depuis le CAS de l'université

### Vuejs

ouvrir un second terminal, puis se placer dans le répertoire « frontend »
installer yarn :

https://classic.yarnpkg.com/en/docs/install#debian-stable

modifier le fichier .env.local à votre besoin, en fonction de l'environnement souhaité

> yarn install

> yarn build

L’application se lance sur http://localhost:8000


_____


L’application comprend trois ensembles :

- core
- matos
- frontend

        Api (core)
      
permet d’interagir avec la plateforme pour accéder et modifier les ressources suivantes :

- gestion du matériel
- Prêts et réservations
- Utilisateurs (provenant de CAS ou enregistré préalablement)
- gestion et accès aux entités

trois rôles sont affectés :
				- utilisateur (accéder aux ressources en lecture)
				- manager (gestion des ressources pour une entité)
				- admin (gestion de l'ensemble de la plateforme)
  

 		Administration 

avec le rôle admin, l'ensemble de la plateforme peut être gérée.
Permettant de :
- créer / modifier et supprimer les entités
- ajouter des utilisateurs et affiliations aux entités
- gérer les catégories de matériels
- gérer les utilisateurs de la plateforme
- gérer les prêts de toutes les entités
- ajouter des managers aux entités

		Manager

chaque entité comporte un ou plusieurs managers, responsable des prêts et des équipements qu'il possède. Il peut gérer les informations de l'entité. 

