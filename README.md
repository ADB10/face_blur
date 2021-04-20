# FaceBlur

## Fonctionnement du logiciel

La partie gauche permet de définir les paramètres, explication des paramètres de haut en bas:

Choisir le dossier des vidéos  
  -> permet de sélectionner le dossier ou se trouve la/les vidéo(s) à flouter (un dossier peut apparaître vide alors qu'il contient des fichiers)

Liste des fichiers dans le dossier des vidéos  
  -> permet de sélectionner la vidéo sur laquelle appliquer le floutage, il est possible de voir la vidéo selectionner dans la partie droite en cliquant sur le bouton "▶"
  
Choisir le dossier de destination  
  -> permet de sélectionner le dossier de destination des vidéos traitées

Flouter  
  -> si coché, floute la vidéo sinon ne floute pas

Format  
  -> permet de sélectionner le format de sortie de la vidéo
  
Rotation  
  -> permet de définir une rotation à la vidéo traitée
     
IPS  
  -> permet de définir le nombre d'images par seconde de la vidéo traitée
    
Sensibilité  
  -> permet de définir la sensibilité de détection des visage (1: très sensible, 9: peu sensible)
    
Appliquer les paramètre pour:  
  -> permet de définir si seule la vidéo sélectionnée est traitée ou alors tout le dossier est traité
    
Nom du fichier  
  -> permet de définir le nom de la vidéo en sortie, si laissé vide "_anonymized" est ajouté: NOM_FICHIER_anonymized.format
    
Appliquer  
  -> une fois appuyé, le traitements des vidéos commence automatiquement et une barre de chargement s'affiche sous le bouton
  
  

## Créer un executable sur Windows 10

Installer python3.6, pip, auto-py-to-exe
Télécharger le code source et installer les dépendances
Lancer la commande "auto-py-to-exe" depuis un terminal

Script location = sélectionner main.py à la racine
Selectionner One Directory
Window Based pour cacher la console
Ajouter des dossiers et des fichiers dans la partie "Additional Files"
Add Folder:
  - thread_video
  - interface
  - deface

Add files:
  - cache.json
  - logs.log
