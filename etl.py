import requests
import psycopg2
import os
import pandas as pd
from dotenv import load_dotenv
import logging

# Configuration du logger
logging.basicConfig(
    filename='etl.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


load_dotenv()

def extract():
    url = "https://jokeapi-v2.p.rapidapi.com/joke/Any"
    querystring = {"format":"json","idRange":"0-318","lang":"fr"}
    headers = {
        "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": os.getenv("RAPIDAPI_HOST")
    }
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erreur {response.status_code} : {response.text}")



def transform(data):
    df = pd.DataFrame([{
        "category": data.get("category"),
        "type": data.get("type"),
        "setup": data.get("setup"),
        "delivery": data.get("delivery"),
        "safe": data.get("safe"),
        "lang": data.get("lang")
    }])
    
    return df


def joke_exists(conn, setup, delivery):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT 1 FROM jokes WHERE setup = %s AND delivery = %s
        """, (setup, delivery))
        return cur.fetchone() is not None

def load(dataframe):
    try:
        conn = psycopg2.connect(
            dbname="etl_db",
            user="etl_user",
            password="EtlUser2024!",
            host="localhost",
            port="5432"
        )

        for _, row in dataframe.iterrows():
            while joke_exists(conn, row['setup'], row['delivery']):
                print("⚠️ Blague déjà existante, nouvelle tentative d’extraction...")
                new_data = extract()
                transformed_df = transform(new_data)
                row = transformed_df.iloc[0]

            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO jokes (category, type, setup, delivery, safe, lang)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    row['category'], row['type'],
                    row['setup'], row['delivery'],
                    row['safe'], row['lang']
                ))
        conn.commit()
        print("✅ Données insérées avec succès dans PostgreSQL.")
    except Exception as e:
        print("⛔ Erreur de chargement PostgreSQL :", e)
    finally:
        conn.close()



if __name__ == "__main__":
    try:
        data = extract()
        logging.info("Extraction réussie.")
        df = transform(data)
        logging.info("Transformation réussie.")
        load(df)
    except ValueError as e:
        logging.warning(f"Type de donnée non accepté : {e}")
    except Exception as e:
        logging.critical(f"Erreur critique dans le pipeline ETL : {e}")

