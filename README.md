# Système de Recherche Textuelle avec Indexation Inversée

Ce projet implémente un système de recherche textuelle basé sur l'indexation inversée et offre une interface interactive via **Dash** pour rechercher des mots ou des expressions dans un corpus de textes. Il génère également des nuages de mots contextuels et fournit des statistiques sur les résultats de la recherche.

## Fonctionnalités principales

- **Recherche de mots et expressions** : Permet de rechercher un mot ou une expression dans un corpus de documents textuels.
- **Affichage des extraits de texte** : Pour chaque occurrence trouvée, le système affiche un extrait de texte autour de l'expression recherchée.
- **Génération d'un nuage de mots** : Génère un nuage de mots à partir des mots contextuels entourant l'expression recherchée.
- **Statistiques détaillées** : Affiche des statistiques sur le nombre total d'apparitions de l'expression, la distribution des occurrences dans les documents et la moyenne des occurrences dans chaque document.

## Technologies utilisées

- **Python** 3.x
- **Dash** : Framework web pour construire des applications interactives en Python.
- **WordCloud** : Bibliothèque pour générer des nuages de mots.
- **pandas** : Manipulation de données et chargement du dataset.
- **nltk** : Traitement du langage naturel (tokenisation, stopwords, lemmatisation).
- **Matplotlib** : Visualisation des données, utilisé pour afficher des graphiques.
- **Base64** : Encodage d'images pour les afficher dans l'interface web.

## Installation

### Prérequis

1. Clonez le repository sur votre machine locale
2. Créez un environnement virtuel et installez les dépendances nécessaires
3. Téléchargement des ressources NLTK
4. Lancer l'application Dash 





