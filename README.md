# face_blur


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

