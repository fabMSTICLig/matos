# Plateforme prêt matériels

## Installation

- git
- python 3 (with pip)
- nodejs


Cloner le dépôt
> git clone https://gricad-gitlab.univ-grenoble-alpes.fr/fabmstic/platepret.git

### Django
ouvrir un terminal,
se positionner à la racine. 

> sudo apt-get update
> sudo apt-get -y upgrade

> sudo apt-get install -y python3-venv

créer l’environnement virtuel

> python3 -m venv venv

activer l’environnement virtuel
> . ./venv/bin/activate

installer les dépendances :
(pour la dépendance générant les pdf, installer les librairies qui suivent avant d'installer avec requirements.txt)
> sudo apt-get install libcairo2-dev pkg-config

> pip install -r requirements.txt

### settings

> cp matos/local_settings.py.example matos/local_settings.py

modifier `matos/local_settings.py` et `matos/settings.py`

appliquer les migrations

> python3 manage.py migrate

démarrer le serveur

> python3 manage.py runserver

### authentification


- sudo python3 manage.py createsuperuser --username=joe --email=joe@example.com
 
### login

> login depuis le CAS de l'université
> login local sur http://localhost:8000/auth/login

### Vuejs

ouvrir un second terminal, puis se placer dans le répertoire « frontend »

installer la dernier version de nodejs avec NVM https://github.com/nvm-sh/nvm#installing-and-updating

modifier le fichier .env et .env.local à votre besoin, en fonction de l'environnement souhaité

> npm install

> npm build

_____

- matos
- frontend

		Api (core)
      
permet d’interagir avec la plateforme pour accéder et modifier les ressources suivantes :

				- utilisateur (accéder aux ressources en lecture)
				- manager (gestion des ressources pour une entité)
				- admin (gestion de l'ensemble de la plateforme)

		Administration

avec le rôle admin, l'ensemble de la plateforme peut être gérée.
Permettant de :
- créer / modifier et supprimer les entités
- ajouter des utilisateurs et affiliations aux entités
- gérer les catégories de matériels
- gérer les utilisateurs de la plateforme
- gérer les prêts de toutes les entités
- ajouter des managers aux entités

		Manager

chaque entité comporte un ou plusieurs managers, responsable des prêts et des équipements qu'il possède. Il peut gérer les informations de l'entité. 