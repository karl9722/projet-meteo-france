# Projet Météo France HABRAN Karl et Cuny Felix



Projet réalisé dans le cadre du module Data Visualization.

## Membres du groupe

- Karl HABRAN — Data Engineering / Backend
- Felix CUNY — Dashboard / Data Analysis

---

# Objectif du projet

L’objectif du projet est d’analyser l’évolution du climat à Paris à partir des données OpenData de Météo France.

Nous avons construit une pipeline complète de traitement de données :

```text
API Météo France
        ↓
ETL Python
        ↓
Nettoyage des données
        ↓
PostgreSQL
        ↓
Vues SQL analytiques
        ↓
Metabase Dashboards

```
--

# Structure du projet

projet-meteo-france/
│
├── dashboard/
│
├── data/
│   └── raw/
│
├── etl/
│   └── import_weather_data.py
│
├── sql/
│   └── create_views.sql
│
├── docker-compose.yml
├── requirements.txt
├── README.md


# Données utilisées

Source :
https://meteo.data.gouv.fr/

Datasets utilisés :

données historiques avant 1949 ;
données modernes ;
températures ;
précipitations ;
stations météo du département 75 (Paris).

Tables PostgreSQL :

weather_historical
weather_modern
climate_comparison




Installation
1. Cloner le projet
git clone <repo-url>
cd projet-meteo-france
2. Lancer Docker
docker compose up -d
3. Installer les dépendances Python
pip install -r requirements.txt
4. Lancer l’ETL
python etl/import_weather_data.py
Accès Metabase

URL :

http://localhost:10000

# Configuration PostgreSQL :

Host: postgres
Port: 5432
Database: meteo_france
Username: admin
Password: admin
Fonctionnalités

# Backend / Data Engineering

récupération automatique des données Météo France ;
téléchargement et décompression des fichiers CSV ;
nettoyage des données ;
conversion des dates ;
import PostgreSQL ;
création de vues analytiques SQL ;
gestion Docker.


# Dashboard / BI
dashboards interactifs Metabase ;
visualisations climatiques ;
storytelling ;
comparaison historique vs moderne ;
analyse des tendances climatiques.



# Méthodologie

Organisation du projet avec une approche agile :

Sprint 1 → setup technique ;
Sprint 2 → ETL et ingestion des données ;
Sprint 3 → nettoyage et analyse ;
Sprint 4 → dashboards Metabase ;
Sprint 5 → storytelling et soutenance.

# Auteurs

Projet réalisé par :

Karl HABRAN
Felix CUNY
