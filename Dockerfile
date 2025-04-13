# Étape 1 : Image de base Python 3.10
FROM python:3.10-slim

# Étape 2 : Répertoire de travail
WORKDIR /app

# Étape 3 : Copier les fichiers
COPY requirements.txt ./
COPY . .

# Étape 4 : Installer les dépendances
RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Étape 5 : Lancer le script principal
CMD ["python", "main.py"]
