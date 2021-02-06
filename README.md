# face_blur


## do list
- [ ] TODO récupérer données de deface pour la barre de progression dans l'interface
- [ ] TODO faire un système de log
- [ ] TODO interface : pop up pour plus de lisibilité ? IHM à revoir
- [ ] TODO interface : nom pour dossier ? (anonymized pour chaque video ?)
- [ ] TODO interface : changer la barre de scroll (changer le pas) sous la video pour afficher chaque image
- [ ] TODO interface : possibilite de rotate la video
- [x] interface : choisir nom + dossier plus facilement (29/01)
- [x] interface : barre de lecture vidéo plus facile d'utilisation et plus lisible (29/01)
- [x] interface : nom pour fichier flouté OK (06/02)
- [x] deface : ne pas utiliser l'executable mais directement le code pour pouvoir mieux l'integrer dans l'interface (19/01)
- [ ] deface : possibilite d'annuler le flouttage
- [x] deface/interface : flouter un dossier
- [ ] interface : animation quand la video charge (pour le moment l'app se bloque quand une video est en train de se faire flouter)
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

