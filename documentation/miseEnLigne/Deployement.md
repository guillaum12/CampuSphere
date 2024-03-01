# Se connecter à la VM (Virtual Machine)

- Demander à ce qu'on ajoute ma clé ssh au serveur puis taper dans Bash :

        ssh ubuntu@campusphere.cs-campus.fr

- Activer l'environnement virtuel : 

        venv


## Infos VM Viarézo

Adresse IP : 138.195.139.59

campusphere.cs-campus.fr

[Charte des VM Viarézo](charteVR.pdf)



## Architecture du serveur 

En arrivant sur le serveur, vous arrivez dans le dossier `/home/ubuntu`. On y trouve le dossier `Convention`, qui contient tous les éléments de Git.

Les configurations de Nginx sont dans `/etc/nginx/`.

Les logs de visite du site se situent dans `/var/log/nginx/access.log` et les erreurs dans `/var/log/nginx/error.log`.


# Mettre en ligne le site

Avant toute chose, cette commande annonce ce qu'il reste à configurer : 
        
        python manage.py check --deploy

Voici les étapes à suivre :

- Sur la VM, créer une clé SSH (`ssh-keygen -t ed25519`) et la déposer sur Github.
- Clone le repo sur le serveur
- Créer un environnement virtuel puis lancer :

        pip install -r requirements.txt


- Effectuer les migrations
- Suivre ce [tutoriel](https://www.youtube.com/watch?v=YnrgBeIRtvo&pbjreload=102) où tout est expliqué.

- Puis :

        /etc/nginx/sites-available/default


Pour tester la configuration Nginx, lancer :

        sudo nginx -t


## Ports

Un parefeu est appliqué par défaut sur les machines : par défaut rien ne passe. 
Il faut donc demander d'ouvrir un port pour utiliser un service associé. Par exemple, le port :
- 80 sert au HTTP
- 443 sert au HTTPS
- 587 permet l'envoi de mail

En cas de doute, installer nmap puis `nmap -v ip_machine` permet de connaître les ports utilisés.

## Fichiers Static

Configurer les settings : 

        STATIC_URL = '/static/'  
        STATIC_ROOT = '/home/ubuntu/static'  
        STATICFILES_DIRS = (  
                os.path.join(BASE_DIR, "static"),  
        )  

Puis lancer :

        python manage.py collectstatic

En cas d'erreur 403, essayer : `sudo usermod -a -G ubuntu www-data` (cette commande permet de donner l'accès à Nginx)

## Sécurité

En cas d'erreur CSRF TOKEN lorsque l'on essaye de se connecter, il faut sans doute aller trifouiller dans settings.py la ligne : CSRF_TRUSTED_ORIGINS.

### HTTPS

Pour mettre en place des connexions sécurisées, suivre ce [tutoriel](https://realpython.com/django-nginx-gunicorn/#making-your-site-production-ready-with-https). 

En résumé :

Bien vérifier que le port 443 est ouvert.

```
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
sudo certbot --nginx --rsa-key-size 4096 --no-redirect
```


### Cron jobs

L'objectif est d'un cron job est d'exécuter des tâches de manière récurrente en arrière plan. [Tuto](https://gutsytechster.wordpress.com/2019/06/24/how-to-setup-a-cron-job-in-django/). Ne fonctionne que sous linux, donc sur le serveur.

Après modifications des CRONJOBS : 

        python manage.py crontab add

Pour afficher les CRONJOBS : 

        python manage.py crontab show

Pour enlever un CRONJOBS :

        python manage.py crontab remove

Ici, on se sert de Cron Jobs pour sauvegarder automatiquement la base de données et l'excel sur le serveur FTP d'OVH.

### Bugs récurrents

Attention, il ne doit pas rester de `print()` dans le code déployer, le serveur n'aime pas ça ! En réalité, il ne sait pas où afficher ce qu'on lui dit d'afficher

# Commandes de base

Commencer par suivre la [formation VR](VMasso.pdf) : 

Pour mettre à jour la VM

        sudo apt update
        sudo apt upgrade

C'est une bonne pratique de le faire régulièrement, notamment pour corriger des failles de sécurité.

Pour relancer le serveur : 

        sudo reboot

# Commandes récurrentes

## Gunicorn

Lancer gunicorn : 

        gunicorn -c ~/conf/gunicorn_config.py Convention.convention.wsgi &

Arrêter gunicorn : 

        pkill gunicorn

Puis CTRL+Z et `bg` pour mettre la tâche à l'arrière plan

## Nginx

Pour configurer Nginx :
        
        sudo nano /etc/nginx/sites-available/Convention


Pour relancer Nginx :

        sudo systemctl restart nginx


## Django

Pour accèder aux settings Python : 

        nano /home/ubuntu/Convention/InscriptionsRaid/settings.py


## Mise en ligne rapide

Toutes ces commandes prennent beaucoup de temps à taper, donc je les ai rassemblé dans un script Bash qui active l'environnement virtuel, récupère la dernière version sur Git, applique les migrations et les `requirements`, puis qui effectue les migrations et finalement relance Gunicorn. Il suffit de lancer :

        source up.sh

puis CTRL + C lorsque Gunicorn est relancé !

## Alias

Un alias est un raccourci pour taper des commandes compliqués rapidement.

Par exemple en tapant 'env' dans le terminal, on active directement l'environnement virtuel.

Suivre ce [tutoriel](https://doc.ubuntu-fr.org/alias) pour approfondir le sujet. Vous pouvez ajouter vos propres alias dans le fichier `.bash_aliases`.

Ne pas oublier d'exécuter `.bashrc` une fois les alias complétés.

Listes des alias configurés :

- `env` : activation de l'environnement virtuel
- `reload` : redémarrage de gunicorn et nginx
- `update` : pull de git, application des migrations et redémarrage

