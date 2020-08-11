# Gestionnaire Bourse (*Boursorama*)
Exécutable permettant de savoir le cours Boursorama, Portefeuille réel et virtuel, Dividende et Liste personnalisée.
La version est pour le moment en ligne de commande très simple à prendre en main.
Une version graphique devrait voir le jour par la suite.

## Exigence
- BeautifulSoup4 ==> 4.9.*+
- Requests ==> 2.24.*+

## Utilisation
- Analyse des valeurs, volumes des actions.
- Créer votre propre liste personnalisée
- Connaitre les dividendes
- Gestion de portefeuille réel et virtuel

## Mise à jour
**V0.4 _(dev)_**
- Ajout CAC40
    - Analyse des sociétés
    - Ajouter dans votre liste
    - Dividendes des sociétés
    - Gestion dans vos portefeuilles

**V0.3**
- Création du portefeuille réel et virtuel
    - "Achat", "Vente", Suppression d'actions
    - Liste des actions possédées
    - Analyse de la perte ou gain suivant le cours
    - Historique de vos achats et vente
- Affichage du cours des actions pour 1 fois, x fois ou jusqu'à la fermeture

**V0.2**
- Ajout d'une base de données local
- Création d'une liste personnalisée
    - Ajout d'une société par code URL
    - Suppression d'une société dans votre liste
    - Voir la liste
- Affichage des dividendes pour les sociétés de votre liste
    - Année en cours
    - Année +1 an
    - Année +2 ans
    - Toutes les années suivant une société précisent

## Idées
- Fichier d'options
    - Choisir le temps d'analyse (60s par défaut)
    - Affichage des données complétes ou partiels
- Analyses des données en fond de tâche
- Importer/Exporter sa liste
- Vérification de la mise à jour
    - Téléchargement si nouvelle version détectée
- Création d'alertes *(valeur, volume échangé, etc..)*
    - Alerte sonore
    - Options sur les son et le volume
- Flux RSS *(alertes et actualités)*
