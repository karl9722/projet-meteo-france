from pathlib import Path
import gzip
import os
import shutil

import pandas as pd
import requests
from sqlalchemy import create_engine


DATASET_API_URL = "https://www.data.gouv.fr/api/1/datasets/donnees-climatologiques-de-base-quotidiennes/"

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://admin:admin@127.0.0.1:5434/meteo_france"
)

DEPARTMENT_CODE = "75"

DATASETS = [
    {
        "keyword": "avant-1949",
        "table": "weather_historical"
    },
    {
        "keyword": "recent",
        "table": "weather_modern"
    }
]


def get_dataset_resources():
    print("Connexion à l'API data.gouv.fr...")
    response = requests.get(DATASET_API_URL, timeout=30)
    response.raise_for_status()
    return response.json()["resources"]


def find_resource(resources, period_keyword):
    print(f"Recherche du fichier météo pour le département {DEPARTMENT_CODE}...")

    for resource in resources:
        title = resource.get("title", "").lower()
        url = resource.get("url", "")

        if (
            DEPARTMENT_CODE in title
            and (
                period_keyword in title
                or "2023" in title
                or "2024" in title
                or "2025" in title
            )
            and url.endswith(".csv.gz")
        ):
           
           
            return url, resource.get("title", "weather data")
        
    

    raise ValueError(f"Aucun fichier CSV.GZ trouvé pour le département {DEPARTMENT_CODE}.")


def download_file(url, output_path):
    print("Téléchargement du fichier...")
    response = requests.get(url, stream=True, timeout=60)
    response.raise_for_status()

    with open(output_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)

    print(f"Fichier téléchargé : {output_path}")


def unzip_file(gz_path, csv_path):
    print("Décompression du fichier...")
    with gzip.open(gz_path, "rb") as file_in:
        with open(csv_path, "wb") as file_out:
            shutil.copyfileobj(file_in, file_out)

    print(f"Fichier décompressé : {csv_path}")


def clean_dataframe(df):
    print("Nettoyage des données...")

    df.columns = (
        df.columns
        .str.lower()
        .str.strip()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    if "aaaammjj" in df.columns:
        df["date"] = pd.to_datetime(
            df["aaaammjj"],
            format="%Y%m%d",
            errors="coerce"
        )

        df = df.dropna(subset=["date"])

    numeric_columns = ["t", "tn", "tx", "rr", "ffm", "fxi"]
    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df.drop_duplicates()

    print(f"Données nettoyées : {len(df)} lignes restantes.")
    return df


def import_to_postgres(csv_path, table_name):
    print("Lecture du CSV...")
    df = pd.read_csv(
        csv_path,
        sep=";",
        encoding="latin1",
        low_memory=False
    )

    df = clean_dataframe(df)

    print("Connexion à PostgreSQL...")
    engine = create_engine(DATABASE_URL)

    print(f"Import dans la table {table_name}...")
    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False,
        chunksize=1000
    )
    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False,
        chunksize=1000
    )

    print(f"{len(df)} lignes importées dans PostgreSQL.")


def main():
    try:
        raw_dir = Path("data/raw")
        raw_dir.mkdir(parents=True, exist_ok=True)

        resources = get_dataset_resources()

        for dataset in DATASETS:

            period_keyword = dataset["keyword"]
            table_name = dataset["table"]

            print("\n===================================")
            print(f"Traitement dataset : {period_keyword}")
            print("===================================\n")

            gz_path = raw_dir / f"{table_name}.csv.gz"
            csv_path = raw_dir / f"{table_name}.csv"

            url, title = find_resource(resources, period_keyword)

            print(f"Dataset sélectionné : {title}")

            download_file(url, gz_path)
            unzip_file(gz_path, csv_path)
            import_to_postgres(csv_path, table_name)

        print("\nETL terminé avec succès.")

    except requests.RequestException as error:
        print(f"Erreur API ou téléchargement : {error}")

    except Exception as error:
        print(f"Erreur pendant l'ETL : {error}")


if __name__ == "__main__":
    main()