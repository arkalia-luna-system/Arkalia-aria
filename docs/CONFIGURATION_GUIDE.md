# Guide de Configuration ARKALIA ARIA

**Dernière mise à jour :** Novembre 2025

---

## 🎯 Objectif

Ce guide explique comment configurer ARKALIA ARIA pour différents environnements (développement, test, production).

---

## Configuration de Base

### Variables d'Environnement
```bash
# Copier le fichier d'exemple
cp env.example .env

# Variables principales
ARIA_DB_PATH=aria_pain.db
ARIA_LOG_LEVEL=INFO
ARIA_MAX_REQUEST_SIZE=10485760
ARIA_CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
ARIA_REDIS_URL=redis://localhost:6379
ARIA_SECRET_KEY=your-secret-key-here
```

### Configuration Centralisée
```python
# core/config.py
from pydantic_settings import BaseSettings

class Config(BaseSettings):
    ARIA_DB_PATH: str = "aria_pain.db"
    ARIA_LOG_LEVEL: str = "INFO"
    ARIA_MAX_REQUEST_SIZE: int = 10485760
    ARIA_CORS_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"
    ARIA_REDIS_URL: str = "redis://localhost:6379"
    ARIA_SECRET_KEY: str = "your-secret-key-here"
    
    class Config:
        env_file = ".env"
```

---

## Environnements

### Développement Local
```bash
# Configuration développement
export ARIA_DB_PATH=aria_pain.db
export ARIA_LOG_LEVEL=DEBUG
export ARIA_MAX_REQUEST_SIZE=10485760
export ARIA_CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
export ARIA_REDIS_URL=redis://localhost:6379
export ARIA_SECRET_KEY=dev-secret-key

# Lancer en mode développement
python main.py
```

### Test/Staging
```bash
# Configuration test
export ARIA_DB_PATH=aria_pain_test.db
export ARIA_LOG_LEVEL=INFO
export ARIA_MAX_REQUEST_SIZE=10485760
export ARIA_CORS_ORIGINS=http://test.arkalia-aria.com
export ARIA_REDIS_URL=redis://test-redis:6379
export ARIA_SECRET_KEY=test-secret-key

# Lancer en mode test
uvicorn main:app --host 0.0.0.0 --port 8001 --workers 2
```

### Production
```bash
# Configuration production
export ARIA_DB_PATH=/app/data/aria_pain.db
export ARIA_LOG_LEVEL=WARNING
export ARIA_MAX_REQUEST_SIZE=10485760
export ARIA_CORS_ORIGINS=https://arkalia-aria.com
export ARIA_REDIS_URL=redis://prod-redis:6379
export ARIA_SECRET_KEY=prod-secret-key

# Lancer en mode production
uvicorn main:app --host 0.0.0.0 --port 8001 --workers 4
```

---

## Base de Données

### SQLite (Développement)
```python
# Configuration SQLite
DATABASE_CONFIG = {
    "type": "sqlite",
    "path": "aria_pain.db",
    "options": {
        "check_same_thread": False,
        "timeout": 30,
        "isolation_level": None
    }
}
```

### PostgreSQL (Production)
```python
# Configuration PostgreSQL
DATABASE_CONFIG = {
    "type": "postgresql",
    "host": "localhost",
    "port": 5432,
    "database": "arkalia_aria",
    "username": "aria_user",
    "password": "aria_password",
    "options": {
        "pool_size": 10,
        "max_overflow": 20,
        "pool_timeout": 30,
        "pool_recycle": 3600
    }
}
```

### MySQL (Alternative)
```python
# Configuration MySQL
DATABASE_CONFIG = {
    "type": "mysql",
    "host": "localhost",
    "port": 3306,
    "database": "arkalia_aria",
    "username": "aria_user",
    "password": "aria_password",
    "options": {
        "pool_size": 10,
        "max_overflow": 20,
        "pool_timeout": 30,
        "pool_recycle": 3600
    }
}
```

---

## Sécurité

### HTTPS/TLS
```nginx
# nginx.conf
server {
    listen 443 ssl http2;
    server_name arkalia-aria.com;
    
    ssl_certificate /etc/ssl/certs/arkalia-aria.crt;
    ssl_certificate_key /etc/ssl/private/arkalia-aria.key;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;
    
    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### CORS
```python
# Configuration CORS
CORS_CONFIG = {
    "allow_origins": [
        "https://arkalia-aria.com",
        "https://app.arkalia-aria.com",
        "https://mobile.arkalia-aria.com"
    ],
    "allow_credentials": True,
    "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["*"],
    "max_age": 3600
}
```

### Rate Limiting
```python
# Configuration Rate Limiting
RATE_LIMIT_CONFIG = {
    "enabled": True,
    "requests_per_minute": 60,
    "burst_size": 10,
    "exclude_paths": ["/health", "/status", "/metrics"]
}
```

---

## Monitoring

### Prometheus
```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'arkalia-aria'
    static_configs:
      - targets: ['localhost:8001']
    metrics_path: '/metrics'
    scrape_interval: 5s
```

### Grafana
```json
{
  "dashboard": {
    "title": "ARKALIA ARIA Monitoring",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{method}} {{endpoint}}"
          }
        ]
      },
      {
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          }
        ]
      }
    ]
  }
}
```

### Logs
```python
# Configuration des logs
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        },
        "detailed": {
            "format": "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "standard",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "filename": "logs/arkalia-aria.log",
            "maxBytes": 10485760,
            "backupCount": 5
        }
    },
    "loggers": {
        "arkalia_aria": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False
        }
    }
}
```

---

## 🐳 **Docker**

### Dockerfile
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers de configuration
COPY requirements.txt .
COPY pyproject.toml .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . .

# Créer les dossiers nécessaires
RUN mkdir -p logs data

# Exposer le port
EXPOSE 8001

# Commande par défaut
CMD ["python", "main.py"]
```

### Docker Compose
```yaml
version: '3.8'

services:
  aria:
    build: .
    ports:
      - "8001:8001"
    environment:
      - ARIA_DB_PATH=/app/data/aria_pain.db
      - ARIA_LOG_LEVEL=INFO
      - ARIA_REDIS_URL=redis://redis:6379
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    depends_on:
      - redis
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./config/nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/ssl
    depends_on:
      - aria
    restart: unless-stopped

volumes:
  redis_data:
```

---

## Configuration Mobile

### Flutter
```yaml
# pubspec.yaml
name: arkalia_aria
description: ARKALIA ARIA Mobile App
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'
  flutter: ">=3.10.0"

dependencies:
  flutter:
    sdk: flutter
  http: ^1.1.0
  shared_preferences: ^2.2.0
  flutter_local_notifications: ^16.0.0

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0
```

### Configuration API
```dart
// lib/config/api_config.dart
class ApiConfig {
  static const String baseUrl = 'https://api.arkalia-aria.com';
  static const String apiVersion = 'v1';
  static const Duration timeout = Duration(seconds: 30);
  
  static String get apiUrl => '$baseUrl/$apiVersion';
}
```

---

## Outils de Développement

### Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
      - id: black
        language_version: python3.10

  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--fix]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.0
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]
```

### Makefile
```makefile
# Makefile
.PHONY: install test lint format clean docker

install:
	pip install -r requirements.txt

test:
	python -m pytest tests/ -v

lint:
	black . && ruff check . --fix && mypy .

format:
	black . && ruff check . --fix

clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +
	rm -rf .pytest_cache htmlcov/

docker:
	docker-compose up --build -d

docker-clean:
	docker-compose down
	docker system prune -f
```

---

## 🚨 **Configuration de Production**

### Checklist Production
- [ ] **HTTPS** - Certificats SSL configurés
- [ ] **Base de données** - PostgreSQL/MySQL configuré
- [ ] **Monitoring** - Prometheus + Grafana actifs
- [ ] **Logs** - Rotation et centralisation
- [ ] **Backups** - Automatiques et testés
- [ ] **Sécurité** - Firewall et rate limiting
- [ ] **Performance** - Cache Redis configuré
- [ ] **Alertes** - Notifications configurées

### Variables d'Environnement Production
```bash
# Production
ARIA_DB_PATH=/app/data/aria_pain.db
ARIA_LOG_LEVEL=WARNING
ARIA_MAX_REQUEST_SIZE=10485760
ARIA_CORS_ORIGINS=https://arkalia-aria.com
ARIA_REDIS_URL=redis://prod-redis:6379
ARIA_SECRET_KEY=prod-secret-key-very-secure
ARIA_DATABASE_URL=postgresql://user:pass@localhost:5432/arkalia_aria
ARIA_SENTRY_DSN=https://your-sentry-dsn
ARIA_PROMETHEUS_ENABLED=true
ARIA_GRAFANA_URL=https://grafana.arkalia-aria.com
```

---

## Configuration par Environnement

### Développement
```bash
# .env.development
ARIA_DB_PATH=aria_pain.db
ARIA_LOG_LEVEL=DEBUG
ARIA_CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
ARIA_REDIS_URL=redis://localhost:6379
ARIA_SECRET_KEY=dev-secret-key
```

### Test
```bash
# .env.test
ARIA_DB_PATH=aria_pain_test.db
ARIA_LOG_LEVEL=INFO
ARIA_CORS_ORIGINS=http://test.arkalia-aria.com
ARIA_REDIS_URL=redis://test-redis:6379
ARIA_SECRET_KEY=test-secret-key
```

### Production
```bash
# .env.production
ARIA_DB_PATH=/app/data/aria_pain.db
ARIA_LOG_LEVEL=WARNING
ARIA_CORS_ORIGINS=https://arkalia-aria.com
ARIA_REDIS_URL=redis://prod-redis:6379
ARIA_SECRET_KEY=prod-secret-key-very-secure
```

---

**ARKALIA ARIA** - Guide de configuration
