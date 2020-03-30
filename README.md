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

lancer les migrations

> sudo python3 manage.py makemigrations
…

> sudo python3 manage.py migrate


### Vuejs

ouvrir un second terminal, puis se placer dans le répertoire « frontend »
installer yarn :

https://classic.yarnpkg.com/en/docs/install#debian-stable

> yarn install

> yarn build

L’application se lance sur http://localhost:8000

_____


L’application comprend deux ensembles :

- api
- adminplatform

        Api
      
permet d’interagir avec la plateforme pour accéder et modifier les ressources suivantes :

- Matériel
- Prêts et réservations
- Utilisateurs (provenant de CAS ou enregistré préalablement)
- Entités

deux rôles sont affectés :
				- utilisateur (accéder aux ressources en lecture)
				- manager (gestion des ressources)
  

            Adminplatform

Composante de gestion de la plateforme. Permet de :
- créer / modifier et supprimer les entités
- ajouter des utilisateurs et affiliations aux entités
- gérer les catégories de matériels
- gérer les utilisateurs de la plateforme
- gérer les prêts de toutes les entités