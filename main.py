import logging
from etl.extract import extract
from etl.transform import transform
from etl.load import load

# Config du logger
logging.basicConfig(
    filename='etl.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    try:
        data = extract()
        logging.info("✅ Extraction réussie.")
        df = transform(data)
        logging.info("✅ Transformation réussie.")
        load(df)
        logging.info("✅ Chargement réussi.")
    except ValueError as e:
        logging.warning(f"⚠️ Type de donnée non accepté : {e}")
    except Exception as e:
        logging.critical(f"⛔ Erreur critique dans le pipeline ETL : {e}")

if __name__ == "__main__":
    main()
