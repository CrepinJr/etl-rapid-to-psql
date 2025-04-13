import unittest
from etl.extract import extract
from etl.transform import transform
from etl.utils import joke_exists
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

class TestETL(unittest.TestCase):

    def test_extract_structure(self):
        data = extract()
        self.assertIn("type", data)
        self.assertIn("category", data)
        self.assertIn("lang", data)
        if data["type"] == "twopart":
            self.assertIn("setup", data)
            self.assertIn("delivery", data)

    def test_transform_dataframe(self):
        data = {
            "category": "Misc",
            "type": "twopart",
            "setup": "Quel est le plus gros dilemme pour un juif?",
            "delivery": "Du jambon gratuit",
            "safe": True,
            "lang": "fr"
        }
        df = transform(data)
        self.assertEqual(df.shape[0], 1)
        self.assertIn("setup", df.columns)
        self.assertIn("delivery", df.columns)

    def test_joke_exists_false(self):
        conn = psycopg2.connect(
            dbname=os.getenv("PG_DATABASE"),
            user=os.getenv("PG_USERNAME"),
            password=os.getenv("PG_PASSWORD"),
            host=os.getenv("PG_HOST"),
            port=os.getenv("PG_PORT")
        )
        exists = joke_exists(conn, "blague test qui n'existe pas", "réponse test")
        self.assertFalse(exists)
        conn.close()

if __name__ == '__main__':
    unittest.main()
