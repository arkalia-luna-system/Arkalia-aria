# ARKALIA ARIA - Dockerfile
FROM python:3.10-slim

# Métadonnées
LABEL maintainer="Arkalia Luna System <arkalia.luna.system@gmail.com>"
LABEL description="ARKALIA ARIA - Research Intelligence Assistant"
LABEL version="1.0.0"

# Variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV ARIA_ENV=production

# Créer un utilisateur non-root
RUN groupadd -r aria && useradd -r -g aria aria

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . .

# Changer les permissions
RUN chown -R aria:aria /app

# Passer à l'utilisateur non-root
USER aria

# Exposer le port
EXPOSE 8001

# Commande de démarrage
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
