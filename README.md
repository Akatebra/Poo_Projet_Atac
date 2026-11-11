# Poo_Projet_Atac
L'objectif de ce projet est de proposer un plugin QGIS qui permet de faire appel au service de calculs d'isochrones de la Géoplateforme. On souhaitera pouvoir paramétrer la requête avec toutes les possibilités offertes par le service, et afficher la réponse dans l'interface cartographique.

Liste des diagrammes attendus pour l'analyse :
Diagramme de cas d'utilisation
Diagramme de classes
Diagramme d'activité ou de séquence

Bibliothèques utilisées :
requests,
PyQt,
PyQGIS

Pour avoir plus d'informations sur les notions, veuillez lire le Wiki, Merci!!!

Ressource sur laquelle je me suis appuyée : https://cartes.gouv.fr/aide/fr/guides-utilisateur/utiliser-les-services-de-la-geoplateforme/calcul-isochrone-isodistance/
Donc, seules les ressources documentées par l’IGN sont proposées par mon plugin.

Version QGIS utilise: 
<img width="695" height="368" alt="Version_QGIS" src="https://github.com/user-attachments/assets/f5160f30-4dc0-4e8f-be39-812454fec185" />

Poo_Projet_Atac

Plugin QGIS qui interroge le service de calcul d'isochrones / isodistances de la Géoplateforme (IGN) et affiche le résultat dans l'interface cartographique de QGIS.

L'objectif du projet est de proposer un plugin qui permet de faire appel à ce service en paramétrant la requête avec toutes les possibilités qu'il offre, et d'afficher la réponse sur la carte.

Statut : plugin expérimental, développé dans un cadre pédagogique. Il n'est pas publié sur le dépôt officiel des extensions QGIS : il ne se trouve donc pas dans Extensions ▸ Installer/Gérer les extensions ▸ Tout. Il s'installe manuellement (voir ci-dessous).

Ce que fait le plugin
Saisie de la longitude / latitude du point de départ, ou sélection du point d'un clic sur la carte (conversion automatique en EPSG:4326).
Choix de la ressource de calcul, du type de coût (time ou distance) et de sa valeur.
Appel du service de la Géoplateforme avec la bibliothèque requests.
Affichage sur la carte de deux couches : l'isochrone (semi-transparente) et le point de départ.
Messages d'erreur clairs (valeurs invalides, point hors zone, service indisponible).

Les ressources proposées sont celles documentées par l'IGN : bdtopo-valhalla et bdtopo-pgr. Ressource sur laquelle je me suis appuyée : https://cartes.gouv.fr/aide/fr/guides-utilisateur/utiliser-les-services-de-la-geoplateforme/calcul-isochrone-isodistance/

Prérequis
QGIS 4.x (version testée : voir la capture ci-dessous). Le plugin déclare qgisMinimumVersion=4.0 et supportsQt6=True.
Une connexion Internet (le service de la Géoplateforme est interrogé en ligne).
Aucune installation de bibliothèque supplémentaire : requests, PyQt et PyQGIS sont fournis avec QGIS.

Version QGIS utilisée :

<img width="695" height="368" alt="Version_QGIS" src="https://github.com/user-attachments/assets/f5160f30-4dc0-4e8f-be39-812454fec185" />
Installation (manuelle)

Le plugin n'étant pas publié, on le copie à la main dans le dossier des extensions de QGIS.

Récupérer le code : sur la page GitHub du dépôt, cliquer sur Code ▸ Download ZIP, puis extraire l'archive (ou cloner le dépôt avec git clone).
Ouvrir le dossier des extensions de QGIS : dans QGIS, menu Préférences ▸ Profils utilisateur ▸ Ouvrir le dossier du profil actif, puis aller dans le dossier python, puis plugins.
Créer le dossier du plugin : dans plugins, créer un dossier nommé exactement isochrone_geoplateforme (sans espace, sans accent, sans tiret).
Copier les fichiers du plugin directement dans ce dossier (pas dans un sous-dossier) :
   isochrone_geoplateforme/
   ├── __init__.py
   ├── metadata.txt
   ├── IsochronePlugin.py
   ├── FenetrePlugin.py
   ├── ClientGeoplateforme.py
   ├── ParametresIsochrone.py
   ├── ResultatIsochrone.py
   └── Point.py
Redémarrer QGIS.
Activer le plugin : Extensions ▸ Installer/Gérer les extensions ▸ Installées, puis cocher Isochrones Géoplateforme.

Le plugin étant marqué experimental, si besoin, cocher Afficher les extensions expérimentales dans l'onglet Paramètres du gestionnaire d'extensions.

Si le plugin n'apparaît pas : ouvrir Affichage ▸ Panneaux ▸ Journal des messages ▸ onglet « Extensions Python ». L'erreur y est écrite (fichier manquant, mauvais nom de dossier, etc.).

Mise à jour : remplacer les fichiers dans le dossier isochrone_geoplateforme, puis redémarrer QGIS.

Utilisation
Ouvrir le menu Extensions ▸ Calculer Isochrone.
Renseigner le point de départ : saisir longitude et latitude, ou cliquer sur Sélectionner un point puis cliquer sur la carte (la fenêtre se cache le temps du clic, puis revient avec les champs remplis).
Choisir la ressource, le type de coût (time en secondes, distance en mètres) et sa valeur (maximum 50 000).
Cliquer sur Lancer le calcul. L'isochrone et le point de départ s'ajoutent à la carte.

Remarques

La couche « Isochrone » est une couche temporaire (en mémoire) : pour la conserver, l'exporter (clic droit sur la couche ▸ Exporter ▸ Sauvegarder les entités sous…) avant de fermer le projet.
Le point de départ est toujours envoyé au service en EPSG:4326, quel que soit le système de coordonnées du projet.
Les points hors de la zone couverte par la ressource provoquent une erreur du service.
Architecture du code

Une classe par fichier :

Fichier	Rôle
Point.py	Un point (lon, lat) : mise en forme pour la requête, création de la couche du point de départ
ParametresIsochrone.py	Les paramètres de la requête ; toDict() produit le dictionnaire envoyé au service (les paramètres non renseignés sont retirés)
ClientGeoplateforme.py	Communication avec le service (getcapabilities, isochrone) avec requests
ResultatIsochrone.py	Le résultat renvoyé par le service ; création de la couche QGIS de l'isochrone
FenetrePlugin.py	La fenêtre PyQt : saisie des paramètres, sélection du point sur la carte, lancement du calcul
IsochronePlugin.py	La classe d'intégration à QGIS : entrée de menu, ouverture de la fenêtre
__init__.py	Point d'entrée de QGIS (classFactory)
metadata.txt	Description du plugin lue par QGIS
Pistes d'amélioration
Paramètres optionnels du service : profil (voiture / piéton), direction, contraintes, unités, format de géométrie, projection.
Informations de la requête dans la table attributaire de la couche.
Export du résultat depuis le plugin.
Prise en charge des géométries MultiPolygon.
Analyse des lieux touchés par l'isochrone (communes, équipements).
Documentation

Pour avoir plus d'informations sur les notions, veuillez lire le Wiki.

Liste des diagrammes réalisés pour l'analyse :

Diagramme de cas d'utilisation
Diagramme de classes
Diagramme de séquence

Bibliothèques utilisées : requests, PyQt, PyQGIS.

Auteur

Ange-Christelle — projet fil rouge, Géodata Paris.



