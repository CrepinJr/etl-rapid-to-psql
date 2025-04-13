import psycopg2
import os
from dotenv import load_dotenv
from etl.extract import extract
from etl.transform import transform
from etl.utils import joke_exists

load_dotenv()

def load(dataframe):
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("PG_DATABASE"),
            user=os.getenv("PG_USERNAME"),
            password=os.getenv("PG_PASSWORD"),
            host=os.getenv("PG_HOST"),
            port=os.getenv("PG_PORT")
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
