import requests
import os
from dotenv import load_dotenv

load_dotenv()

def extract():
    url = "https://jokeapi-v2.p.rapidapi.com/joke/Any"
    querystring = {"format": "json", "idRange": "0-318", "lang": "fr"}
    headers = {
        "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": os.getenv("RAPIDAPI_HOST")
    }
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erreur {response.status_code} : {response.text}")
