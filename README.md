# Bénin Insights Challenge 2026

Projet du hackathon iSHEERO × DataCamp Donates autour des données GDELT sur les 12 derniers mois liés au Bénin. L'objectif est de transformer un flux d'événements mondiaux en informations utiles pour un journaliste, un chercheur ou un décideur public, avec un pipeline reproductible, un notebook d'analyse et un dashboard de restitution.

## Description et contexte

GDELT surveille en continu la presse mondiale et documente des événements géopolitiques, sécuritaires et diplomatiques. Dans ce projet, nous nous concentrons sur le Bénin afin d'identifier les dynamiques de sécurité intérieure, les zones de tension, les acteurs récurrents et les signaux de criminalité organisée ou transfrontalière.

Le notebook d'exploration s'appuie sur le jeu de données nettoyé issu de BigQuery et fait ressortir plusieurs tendances fortes : un pic d'activité en décembre 2025, une concentration géographique dans le nord du pays, une part importante d'événements conflictuels et une couverture médiatique marquée par des acteurs comme `TERRORIST`, `POLICE` et `PRISON`.

## Résultats clés du notebook

- 23 859 événements liés au Bénin sur les 12 derniers mois.
- 36,3 % d'événements de nature conflictuelle.
- Un pic net en décembre 2025 avec 4 221 événements.
- Une concentration des signaux de risque dans le nord du pays, notamment vers Atacora, Porga, Malanville, Kandi, Karimama et Natitingou.
- 19,9 % d'acteurs non identifiés (`UNKNOWN`), ce qui confirme la difficulté à attribuer certains réseaux.
- Une couverture médiatique globalement négative ou sous tension sur la période étudiée.

## Structure du projet

```text
.
├── README.md
├── requirements.txt
├── data/
│   ├── raw/
│   │   ├── bq-results-last-12-months.csv
│   │   └── articles/
│   └── clean/
│       ├── clean_gdelt_benin.py
│       ├── bq-results-last-12-months-clean.csv
│       ├── gdelt_benin_clean.parquet
│       └── fichiers d'analyse générés
├── notebooks/
│   └── Analyse exploratoire avec pipeline GDELT.ipynb
├── dashboard/
└── models/
```

### Fichiers importants

- [Notebook principal + Prédiction](notebooks/Analyse%20exploratoire%20avec%20pipeline%20GDELT.ipynb)
- [Script de nettoyage](data/clean/clean_gdelt_benin.py)
- [Données nettoyées CSV](data/clean/bq-results-last-12-months-clean.csv)
- [Archive d'articles scrappés](https://drive.google.com/file/d/1DBkHspEk6mpQ3wii2SuV4-TcJqob4fz0/view?usp=sharing)
- [Dashboard en ligne](https://hackaton-isheero-datacamp-2026-team-8-dashboard.streamlit.app/)
- [Drive de la vidéo](https://drive.google.com/drive/folders/1LLnVvy11NiYAhRzChac474sx4uYFiyhP?usp=sharing)

## Guide de prise en main

### 1. Cloner le dépôt

```bash
git clone https://github.com/Romaric-py/hackaton-isheero-datacamp-2026-team-8.git
```

Ou, si vous utilisez SSH :

```bash
git clone git@github.com:Romaric-py/hackaton-isheero-datacamp-2026-team-8.git
```

### 2. Préparer l'environnement Python

Depuis la racine du projet :

```bash
cd hackaton-isheero-datacamp-2026-team-8
python -m venv .venv
```

Activer ensuite l'environnement virtuel :

Sous Linux / macOS :

```bash
source .venv/bin/activate
```

Sous Windows :

```bash
.venv\\Scripts\\activate
```

Installer les dépendances :

```bash
python -m pip install -r requirements.txt
```

Pour désactiver l'environnement virtuel, utilisez :

```bash
deactivate
```

### 3. Lancer le notebook

Avec l'environnement virtuel activé :

```bash
jupyter notebook
```

Puis ouvrez le dossier `notebooks/` et lancez `Analyse exploratoire avec pipeline GDELT.ipynb`.

### 4. Lancer le dashboard

Le dossier `dashboard/` est prévu pour l'application Streamlit du projet. Si votre version du dépôt contient le point d'entrée `dashboard/app.py`, lancez :

```bash
streamlit run dashboard/app.py
```

Vous pouvez aussi vous placer dans `dashboard/` puis exécuter :

```bash
streamlit run app.py
```

L'application s'ouvre normalement sur `http://localhost:8501`.

## Nettoyage des données

Le nettoyage du fichier brut est assuré par le script :

- `data/clean/clean_gdelt_benin.py`

Ce script :

- charge le fichier brut `data/raw/bq-results-last-12-months.csv` ;
- convertit les colonnes de date et de score ;
- standardise les variables numériques utiles ;
- supprime les doublons exacts et ceux basés sur `GLOBALEVENTID` ;
- remplace les valeurs textuelles manquantes par `UNKNOWN` ;
- exporte le dataset nettoyé dans `data/clean/bq-results-last-12-months-clean.csv`.

Exécution :

```bash
python data/clean/clean_gdelt_benin.py
```

## Notebook d'analyse

Le notebook [Analyse exploratoire avec pipeline GDELT](notebooks/Analyse%20exploratoire%20avec%20pipeline%20GDELT.ipynb) couvre :

- le chargement et la préparation des données ;
- les distributions temporelles ;
- la répartition des événements par nature (`QuadClass`) ;
- l'analyse des acteurs et des localisations ;
- le focus sécurité et criminalité organisée ;
- une conclusion orientée vers la Phase 2 du hackathon.

Le notebook met en évidence une lecture claire du terrain : une tension concentrée dans le nord du Bénin, des événements majoritairement verbaux mais avec des signaux conflictuels notables, et une couverture médiatique qui justifie un approfondissement sur la sécurité intérieure et les trafics transfrontaliers.

## Contributeurs

- Abidé Nabik — Data Engineer
- Grâce Mexiale — Data Analyst
- Hervé Kouton — Data Scientist
- Romaric Assogba — ML Engineer

## Outils IA

Ce projet a été assisté avec :

- Claude
- Gemini
- ChatGPT
- GitHub Copilot

## Reproductibilité

Le projet a été structuré pour rester simple à relancer : un environnement virtuel Python, un script de nettoyage unique, un notebook d'exploration principal et un dossier dédié au dashboard. Pour toute réexécution, partez du dépôt propre, installez les dépendances puis relancez le script de nettoyage avant d'ouvrir le notebook ou le dashboard.
