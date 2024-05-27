# CampuSphère

## Comment lancer le site web en local ?

1) Créer un environnement virtuel : `python -m venv env` puis `source env/scripts/activate` (remplacer 'scripts' par 'bin' sous Mac ou Linux)
2) Installer les packages `pip install -r requirements/base.txt`
3) Faire les migrations : `python manage.py makemigrations` puis `python manage.py migrate`
4) Lancer le serveur en local grâce à : `python manage.py runserver`
puis se rendre à http://127.0.0.1:8000/

Lors de la production, pour gagner du temps, la commande `source mi.sh` permet de créer les migrations, les appliquer et lancer le serveur. (Bien penser à activer son environnement avant)


## Prise en main du site

Voici comment se former et comprendre le site : [Prise en main](documentation/Prise%20en%20main.md)


## Deploiement 

Voici comment déployer le site : [Mise en ligne](documentation/miseEnLigne/Deployement.md)


## Contributeurs à contacter au besoin :

 - Guillaume Machabert - guillaume.machabert@student-cs.fr
 - Alexandre Faure - alexandre.faure@student-cs.fr


## Pour plus tard

![Pytest](https://github.com/hatredholder/Social-Network/workflows/tests/badge.svg) [![Coverage Status](https://coveralls.io/repos/github/hatredholder/Social-Network/badge.svg?branch=main)](https://coveralls.io/github/hatredholder/Social-Network?branch=main)


Create a **PostgreSQL** database

```
CREATE DATABASE socialnetworkdb;
```

Create a **.env** file with enviroment variables of `APP_SECRET, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT`

```
APP_SECRET=your_very_very_secure_secret_key
DB_NAME=socialnetworkdb
DB_USER=user
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
``` 

Apply migrations to the database and run the **Django** server 

```
python manage.py migrate 
python manage.py runserver
```  

## Testing

To use the **tests** you need to install **local** module requirements first, to do that, use:
```
pip install -r requirements/local.txt
```

To run the **tests** and check the **coverage** use:
```
pytest --cov
```

To generate an HTML **coverage** report use:
```
pytest --cov-report html:cov_html --cov
```

And finally to test the **code quality** (see if there are any PEP8 errors) use:
```
flake8
```

## Technologies

Frontend: CSS, Semantic UI.

Backend: Django, JavaScript and AJAX.
