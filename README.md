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


## do list
- [x] Choisir le nombre de fps
- [x] changer la barre de scroll (changer le pas) sous la video pour afficher chaque image
- [x] possibilite de rotate la video
- [x] deface : possibilite d'annuler le flouttage
- [x] Choisir format (27/02)
- [x] récupérer données de deface pour la barre de progression dans l'interface
- [x] faire un système de log
- [x] nom pour dossier et fichiers
- [x] interface : choisir nom + dossier plus facilement (29/01)
- [x] interface : barre de lecture vidéo plus facile d'utilisation et plus lisible (29/01)
- [x] interface : nom pour fichier flouté OK (06/02)
- [x] deface : ne pas utiliser l'executable mais directement le code pour pouvoir mieux l'integrer dans l'interface (19/01)
- [x] deface/interface : flouter un dossier
- [x] interface : animation quand la video charge (pour le moment l'app se bloque quand une video est en train de se faire flouter)
- [x] builder [WORK] (21/01)
- [x] deface : ajout de la possibilité de flouter (19/01)
- [x] interface : bloc fichier [OK] (15/01)
- [x] interface : bloc video mais manque des choses (15/01)
- [x] interface : fichier (13/01)
- [x] choix dossier destination floutage (19/01)
- [x] bouton play/pause fonctionnel (19/01)

## notes 
#### 20/01/21
- ajout d'un premier builder qui fait marcher l'interface avec les images cependant deface ne fonctionne pas (j'ai utilisé le pip auto-py-to-exe pour le builder)

#### 19/01/21
- utiliser FULL CAPS comprenhsible pour les keys de l'interface (ex: PLay -> PLAY_BUTTON)
- modif emplacement main (dans le root) pour simplifier les chemins d'acces
- ajout boutton flouter (fonctionne)
- transforme video_path en attribut de classe (plus simple pour l'utiliser partout, il faut penser a mettre None quand pas de video select)

