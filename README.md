# Poo_Projet_Atac
Plugin QGIS qui interroge le service de calcul d'isochrones / isodistances de la Géoplateforme (IGN) et affiche le résultat dans l'interface cartographique de QGIS.

L'objectif de ce projet est de proposer un plugin QGIS qui permet de faire appel au service de calculs d'isochrones de la Géoplateforme. On souhaitera pouvoir paramétrer la requête avec toutes les possibilités offertes par le service, et afficher la réponse dans l'interface cartographique.

Statut : plugin expérimental, développé dans un cadre pédagogique. 
Il n'est pas publié sur le dépôt officiel des extensions QGIS : il ne se trouve donc pas dans Extensions ▸ Installer/Gérer les extensions ▸ Tout. Il s'installe manuellement (voir ci-dessous).

Récupérer le code sur la page GitHub du dépôt ou cloner le dépôt avec git clone.
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

Mise à jour : remplacer les fichiers dans le dossier isochrone_geoplateforme, puis redémarrer QGIS.

Les ressources proposées sont celles documentées par l'IGN : bdtopo-valhalla et bdtopo-pgr. Ressource sur laquelle je me suis appuyée : https://cartes.gouv.fr/aide/fr/guides-utilisateur/utiliser-les-services-de-la-geoplateforme/calcul-isochrone-isodistance/

Prérequis
QGIS 4.x (version testée : voir la capture ci-dessous). Le plugin déclare qgisMinimumVersion=4.0 et supportsQt6=True.
Une connexion Internet (le service de la Géoplateforme est interrogé en ligne).
Aucune installation de bibliothèque supplémentaire : requests, PyQt et PyQGIS sont fournis avec QGIS.

Version QGIS utilise: 
<img width="695" height="368" alt="Version_QGIS" src="https://github.com/user-attachments/assets/f5160f30-4dc0-4e8f-be39-812454fec185" />

#### Utilisation
Ouvrir le menu Extensions ▸ Calculer Isochrone.
Renseigner le point de départ : saisir longitude et latitude, ou cliquer sur Sélectionner un point puis cliquer sur la carte.
Choisir la ressource, le type de coût (time en secondes, distance en mètres) et sa valeur (maximum 50 000).
Cliquer sur Lancer le calcul. L'isochrone et le point de départ s'ajoutent à la carte.

#### remarques: 
Le point de départ est toujours envoyé au service en EPSG:4326, quel que soit le système de coordonnées du projet.
Les points hors de la zone couverte par la ressource provoquent une erreur du service.


#### Liste des diagrammes :
Diagramme de cas d'utilisation
Diagramme de classes
Diagramme d'activité ou de séquence

#### Bibliothèques utilisées :
requests,
PyQt,
PyQGIS

#### Pour avoir plus d'informations sur les notions, veuillez lire le Wiki, Merci!!!

Auteur : Ange-Christelle Aka - projet Poo, Géodata Paris.



