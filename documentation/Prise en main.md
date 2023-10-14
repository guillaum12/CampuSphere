# Comment prendre en main le site ?

## HTML & CSS

Ces langages sont les briques élementaires pour créer une page web.

- Le HTML décrit la structure de la page. Il s'agit surtout de comprendre comment fonctionne les balises. Par exemple, `<p>` est un paragraphe et `<a>` est un lien.
- Le CSS permet de créer les styles : couleurs, police d'écriture, style d'un bouton... Ici Bootstrap s'occupe de créer le CSS à notre place (cf section Bootstrap).

## Django 

Tout d'abord, il faut comprendre comment fonctionne Django. Ce framework Python permet de créer le Back du serveur, par opposition au Front. Le Django s'exécute toujours sur le serveur, puis renvoit les pages Web au client. 


Voici un premier tutoriel obligatoire : [Django débutant](https://openclassrooms.com/fr/courses/7172076-debutez-avec-le-framework-django)

Pour aller plus loin, nous avons suivi : [Django avancé](https://openclassrooms.com/fr/courses/7192426-allez-plus-loin-avec-le-framework-django)

Pour faire des requêtes SQL précises, voici : [Advanced models](https://masteringdjango.com/django-tutorials/mastering-django-advanced-models/)

## Architecture du code

... TO DO ...


Chaque application contient :

- un dossier `templates` qui contient les templates HTML.
- un dossier `static` où il faut déposer les images, PDF et script Javascript.
- un fichier `url.py` où l'on indique vers quelle fonction de view chaque url doit rediriger.

et éventuellement

- un fichier `views.py` qui contient le code Python exécuté par le serveur lorsqu'un url est appelé. Une fonction renvoit généralement une page Web qui est envoyé au client.
- un fichier `models.py` qui permet de créer et gérer les tables SQL
- un fichier `form.py` qui gère les formulaires
- un fichier `admin.py` qui permet de gérer l'interface admin (à distinguer de l'interface staff)

Nous n'avons pas touché aux fichiers `apps.py` et `test.py`, qui sont crées automatiquement lors de la création d'une application. 

Le dossier `media` permet de stocker les fichiers envoyés par les utilisateurs. Il est dans le ``.gitignore``

## Interface admin

On accède à cette interface avec `/admin` afin de modifier des éléments précis de la base de données. C'est notamment utile afin de donner aux responsables concurrents la possibilité d'accèder à l'interface `staff` en réglant sur leur profil `is_staff` à `True`.

## Bootstrap

Bootstrap permet de simplifier l'application du CSS. Pour se faire, on modifie la classe d'une balise HTML.

Par exemple, `<a class="btn">` donne à la balise `<a>` le style d'un bouton.

Le Bootstrap est très important pour créer la structure globale du site Web, afin d'agencer correctement les éléments. 

Voici la documentation [Bootstrap 5](https://getbootstrap.com/docs/5.3/getting-started/introduction/)

Voici un [tutoriel](https://openclassrooms.com/fr/courses/7542506-creez-des-sites-web-responsives-avec-bootstrap-5) à feuilleter pour comprendre Bootstrap

### Migration

Attention ! Nous utilisons ici Bootstrap 5. Bootstrap a donc changé 5 fois de version. A chaque changement, certaines fonctionnalités ne fonctionnent plus, et d'autres sont créées. 

Lorsque vous souhaitez ajouter un nouveau composant Bootstrap, faites attention qu'il soit bien compatible avec Bootstrap 5. Plus [d'infos](https://getbootstrap.com/docs/5.0/migration/)

Par exemple, un [collapse](https://getbootstrap.com/docs/4.0/components/collapse/) ne fonctionnait pas car il utilisait une syntaxe Bootstrap 4. J'ai effectué les modifications suivantes :  

data-toggle -> data-bs-toggle  
data-target -> data-bs-target  

et tout fonctionnait à nouveau !

## Crispy

Bootstrap ne permet pas de gérer les designs des formulaires : et c'est là que Crispy rentre en jeu !
Il gère l'agencement des formulaires et leur style.


## VS Code

Si vous utilisez VS Code, installez les extensions suivantes qui vous simplifieront la vie :

- ``Git`` pour manipuler facilement Git
- ``vscode-pdf`` pour lire les PDFs
- ``Django`` pour avoir un code en couleur et identifier les erreurs avant même de le tester

## Mise en ligne

Désormais, tu peux t'intéresser à la [mise en ligne](miseEnLigne/Deployement.md) du site web, qui te sera très utile si le serveur ne fonctionne plus...

# Points d'amélioration

Le site web est aujourd'hui fonctionnel, mais nécessite encore de nombreuses améliorations. Ce qu'il reste à faire est contenu dans un Excel `Gestion des tâches`