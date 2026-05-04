[Lien vers les articles scrapés](https://drive.google.com/file/d/1DBkHspEk6mpQ3wii2SuV4-TcJqob4fz0/view?usp=sharing)

# Bénin Insights Challenge

## Objectif
Projet hackathon orienté sur l'état de sécurité du Bénin, construit autour d'un pipeline GDELT reproductible, d'une analyse exploratoire et d'un dashboard interactif.

## Nettoyage des données
Le nettoyage des données est réalisé par le script :

- `data/clean/clean_gdelt_benin.py`

### Étapes réalisées
- Chargement du fichier brut : `data/raw/bq-results-last-12-months.csv`
- Conversion de `SQLDATE` en format `datetime` (`YYYY-MM-DD`).
- Conversion de `GoldsteinScale` et `AvgTone` en valeurs numériques.
- Conversion des colonnes numériques utiles (`NumMentions`, `NumSources`, `NumArticles`, `Year`, `MonthYear`, `EventCode`, `EventBaseCode`, `EventRootCode`, `QuadClass`).
- Suppression des doublons exacts et des doublons sur `GLOBALEVENTID`. Aucun doublon
- Remplacement des valeurs manquantes de type texte par `UNKNOWN` pour éviter des erreurs de lecture ultérieures.
- Sauvegarde du jeu de données nettoyé dans : `data/clean/bq-results-last-12-months-clean.csv`

## Fichier nettoyé
- `data/clean/bq-results-last-12-months-clean.csv`

## Notebook d'analyse exploratoire
- `notebooks/01_eda.ipynb`

## Exécution
Pour recréer le fichier nettoyé :

```bash
python data/clean/clean_gdelt_benin.py
```
Initial rows: 23859
Final rows: 23859
Removed rows: 0

## Note IA
Ce nettoyage a été assisté par GitHub Copilot pour accélérer l'implémentation et garantir une documentation claire.
